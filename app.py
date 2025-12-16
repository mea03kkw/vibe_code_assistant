#!/usr/bin/env python3
"""
Vibe Code Assistant - Custom Project Builder (Enhanced Version)
A Flask-based web application for generating customized development project plans.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
import zipfile
import tempfile
import logging
import re
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vibe_code_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vibe-code-assistant-secret-key-2025')

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Project(db.Model):
    """Model for storing project configurations"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    project_type = db.Column(db.String(50), nullable=False)
    timeline = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    tech_stack = db.Column(db.Text, nullable=True)
    features = db.Column(db.Text, nullable=True)
    deployment_platform = db.Column(db.String(50), default='github')
    repo_name = db.Column(db.String(100))
    include_readme = db.Column(db.Boolean, default=True)
    include_license = db.Column(db.Boolean, default=False)
    include_gitignore = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert project to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_type': self.project_type,
            'timeline': self.timeline,
            'difficulty': self.difficulty,
            'tech_stack': json.loads(self.tech_stack) if self.tech_stack else {},
            'features': json.loads(self.features) if self.features else [],
            'deployment_platform': self.deployment_platform,
            'repo_name': self.repo_name,
            'include_readme': self.include_readme,
            'include_license': self.include_license,
            'include_gitignore': self.include_gitignore,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Default tech stack options
DEFAULT_TECH_STACKS = {
    'frontend': [
        'React', 'Vue.js', 'Angular', 'Svelte', 'Next.js', 'Nuxt.js',
        'HTML/CSS/JS', 'TypeScript', 'Tailwind CSS', 'Bootstrap', 'Material UI'
    ],
    'backend': [
        'Node.js', 'Express', 'Python', 'Flask', 'Django', 'FastAPI',
        'Ruby on Rails', 'Spring Boot', 'Laravel', 'ASP.NET', 'Go', 'Rust'
    ],
    'database': [
        'PostgreSQL', 'MySQL', 'MongoDB', 'SQLite', 'Redis', 'Firebase',
        'Supabase', 'GraphQL', 'Elasticsearch'
    ],
    'tools': [
        'Docker', 'Git', 'GitHub Actions', 'Jest', 'Cypress', 'Webpack',
        'Vite', 'Ollama', 'OpenAI API'
    ]
}

# Default features
DEFAULT_FEATURES = [
    'Authentication (OAuth, JWT, sessions)',
    'Admin Panel',
    'AI Integration (ChatGPT, local models)',
    'Real-time features (WebSockets)',
    'CRUD Operations',
    'Analytics & Statistics',
    'File Upload',
    'Payment Integration'
]

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

def validate_project_data(data):
    """Validate project configuration data"""
    required_fields = ['project_type', 'timeline', 'difficulty']
    
    # Check required fields
    for field in required_fields:
        if not data.get(field):
            return False, f'Missing required field: {field}'
    
    # Validate project type
    valid_types = ['fullstack', 'frontend', 'backend']
    if data['project_type'] not in valid_types:
        return False, f'Invalid project type: {data["project_type"]}'
    
    # Validate timeline
    valid_timelines = ['weekend', '1week', '2weeks', '1month', '3months', 'open']
    if data['timeline'] not in valid_timelines:
        return False, f'Invalid timeline: {data["timeline"]}'
    
    # Validate difficulty
    valid_difficulties = ['beginner', 'intermediate', 'advanced', 'expert']
    if data['difficulty'] not in valid_difficulties:
        return False, f'Invalid difficulty: {data["difficulty"]}'
    
    return True, None

# Routes
@app.route('/')
def index():
    """Main page with project creation interface"""
    return render_template('index.html')

@app.route('/api/tech-stacks')
def get_tech_stacks():
    """Get available tech stack options"""
    try:
        return jsonify(DEFAULT_TECH_STACKS)
    except Exception as e:
        logger.error(f"Error getting tech stacks: {e}")
        return jsonify({'error': 'Failed to load tech stacks'}), 500

@app.route('/api/features')
def get_features():
    """Get available features"""
    try:
        return jsonify(DEFAULT_FEATURES)
    except Exception as e:
        logger.error(f"Error getting features: {e}")
        return jsonify({'error': 'Failed to load features'}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project configuration"""
    try:
        logger.info("Received request to create project")
        data = request.get_json()
        logger.info(f"Request data: {data}")

        # Validate input data
        is_valid, error_msg = validate_project_data(data)
        if not is_valid:
            logger.error(f"Validation failed: {error_msg}")
            return jsonify({'error': error_msg}), 400

        # Calculate timeline days
        timeline_value = data.get('timeline', '1week')
        timeline_days = 7
        if timeline_value == 'weekend':
            timeline_days = 3
        elif timeline_value == '1week':
            timeline_days = 7
        elif timeline_value == '2weeks':
            timeline_days = 14
        elif timeline_value == '1month':
            timeline_days = 30
        elif timeline_value == '3months':
            timeline_days = 90
        elif timeline_value == 'open':
            timeline_days = 0

        logger.info(f"Creating project with timeline_days: {timeline_days}")

        project = Project(
            title=data.get('title') or 'Untitled Project',
            description=data.get('description') or '',
            project_type=data['project_type'],
            timeline=data['timeline'],
            difficulty=data['difficulty'],
            tech_stack=json.dumps(data.get('tech_stack', {})),
            features=json.dumps(data.get('features', [])),
            deployment_platform=data.get('deployment_platform', 'github'),
            repo_name=data.get('repo_name', ''),
            include_readme=data.get('include_readme', True),
            include_license=data.get('include_license', False),
            include_gitignore=data.get('include_gitignore', True)
        )

        logger.info("Adding project to database")
        db.session.add(project)
        db.session.commit()

        logger.info(f"Project created successfully: {project.id}")

        return jsonify({
            'success': True,
            'project': project.to_dict(),
            'message': 'Project created successfully'
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating project: {e}", exc_info=True)
        return jsonify({'error': f'Failed to create project: {str(e)}'}), 500

@app.route('/api/projects/<int:project_id>')
def get_project(project_id):
    """Get a specific project"""
    try:
        project = Project.query.get_or_404(project_id)
        return jsonify(project.to_dict())
    except Exception as e:
        logger.error(f"Error getting project {project_id}: {e}")
        return jsonify({'error': 'Project not found'}), 404

@app.route('/api/projects')
def get_projects():
    """Get all projects"""
    try:
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return jsonify([project.to_dict() for project in projects])
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        return jsonify({'error': 'Failed to retrieve projects'}), 500

@app.route('/api/generate', methods=['POST'])
def generate_project():
    """Generate detailed project plan"""
    try:
        logger.info("Received request to generate project plan")
        data = request.get_json()
        project_data = data.get('project', {})
        logger.info(f"Project data keys: {list(project_data.keys())}")

        # Generate project plan
        plan = generate_project_plan(project_data)
        logger.info("Project plan generated successfully")

        return jsonify({
            'success': True,
            'plan': plan
        })

    except Exception as e:
        logger.error(f"Error generating project: {e}", exc_info=True)
        return jsonify({'error': f'Failed to generate project plan: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def download_project():
    """Generate and download project files as ZIP"""
    try:
        logger.info("Received request to download project files")
        data = request.get_json()
        project_data = data.get('project', {})
        logger.info(f"Download request for project: {project_data.get('title', 'Untitled')}")

        # Generate project plan
        plan = generate_project_plan(project_data)

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            logger.info(f"Created temp directory: {temp_dir}")

            # Create project directory
            repo_name = re.sub(r'[^\w\-_]', '', project_data.get('repo_name', 'my-project').lower().replace(' ', '-'))
            project_dir = temp_path / repo_name
            project_dir.mkdir(exist_ok=True)
            logger.info(f"Created project directory: {repo_name}")

            # Generate files based on project type
            generate_project_files(project_data, project_dir, plan)
            logger.info("Project files generated")

            # Create ZIP file
            zip_path = temp_path / f"{repo_name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(project_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(project_dir)
                        zipf.write(file_path, arc_name)
            logger.info(f"ZIP file created: {zip_path}")

            # Return ZIP file
            return send_file(
                zip_path,
                as_attachment=True,
                download_name=f"{repo_name}.zip",
                mimetype='application/zip'
            )

    except Exception as e:
        logger.error(f"Error downloading project: {e}", exc_info=True)
        return jsonify({'error': f'Failed to generate project files: {str(e)}'}), 500

def generate_project_files(project_data, project_dir, plan):
    """Generate project files based on configuration"""
    repo_name = re.sub(r'[^\w\-_]', '', project_data.get('repo_name', 'my-project').lower().replace(' ', '-'))
    
    # Create basic project structure
    if project_data.get('project_type') == 'fullstack':
        # Frontend directory
        frontend_dir = project_dir / 'frontend'
        frontend_dir.mkdir(exist_ok=True)
        
        # Backend directory
        backend_dir = project_dir / 'backend'
        backend_dir.mkdir(exist_ok=True)
        
        # Database directory
        db_dir = project_dir / 'database'
        db_dir.mkdir(exist_ok=True)
        
        # Generate frontend files
        generate_frontend_files(project_data, frontend_dir)
        
        # Generate backend files
        generate_backend_files(project_data, backend_dir)
        
    elif project_data.get('project_type') == 'frontend':
        # Single frontend project
        generate_frontend_files(project_data, project_dir)
        
    elif project_data.get('project_type') == 'backend':
        # Single backend project
        generate_backend_files(project_data, project_dir)
    
    # Generate common files
    generate_common_files(project_data, project_dir, plan)

def generate_frontend_files(project_data, frontend_dir):
    """Generate frontend project files"""
    tech_stack = project_data.get('tech_stack', {})
    frontend_tech = tech_stack.get('frontend', [])
    
    # package.json for React/Vue/Angular projects
    if any(tech in frontend_tech for tech in ['React', 'Vue.js', 'Angular']):
        package_json = {
            "name": "frontend",
            "version": "0.1.0",
            "private": True,
            "scripts": {},
            "dependencies": {},
            "devDependencies": {}
        }
        
        # Add scripts and dependencies based on tech stack
        if 'React' in frontend_tech:
            package_json["scripts"]["start"] = "react-scripts start"
            package_json["scripts"]["build"] = "react-scripts build"
            package_json["scripts"]["test"] = "react-scripts test"
            package_json["dependencies"]["react"] = "^18.2.0"
            package_json["dependencies"]["react-dom"] = "^18.2.0"
            package_json["devDependencies"]["react-scripts"] = "5.0.1"
        
        with open(frontend_dir / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
    
    # src directory structure
    src_dir = frontend_dir / 'src'
    src_dir.mkdir(exist_ok=True)
    
    # Basic index.html
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My App</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>"""
    
    with open(frontend_dir / 'index.html', 'w') as f:
        f.write(index_html)

def generate_backend_files(project_data, backend_dir):
    """Generate backend project files"""
    tech_stack = project_data.get('tech_stack', {})
    backend_tech = tech_stack.get('backend', [])
    
    # requirements.txt for Python projects
    if any(tech in backend_tech for tech in ['Python', 'Flask', 'Django', 'FastAPI']):
        requirements = ["flask==2.3.3", "flask-cors==4.0.0", "python-dotenv==1.0.0"]
        with open(backend_dir / 'requirements.txt', 'w') as f:
            f.write('\n'.join(requirements))
    
    # package.json for Node.js projects
    if any(tech in backend_tech for tech in ['Node.js', 'Express']):
        package_json = {
            "name": "backend",
            "version": "1.0.0",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "dotenv": "^16.3.1"
            },
            "devDependencies": {
                "nodemon": "^3.0.1"
            }
        }
        
        with open(backend_dir / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)

def generate_common_files(project_data, project_dir, plan):
    """Generate common project files"""
    
    # README.md
    if project_data.get('include_readme', True):
        with open(project_dir / 'README.md', 'w') as f:
            f.write(plan)
    
    # .gitignore
    if project_data.get('include_gitignore', True):
        gitignore_content = """# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
build/
dist/
"""
        with open(project_dir / '.gitignore', 'w') as f:
            f.write(gitignore_content)
    
    # LICENSE
    if project_data.get('include_license', False):
        license_content = """MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open(project_dir / 'LICENSE', 'w') as f:
            f.write(license_content)
    
    # .env.example
    env_example = """# Environment Configuration
NODE_ENV=development
PORT=3000
DATABASE_URL=sqlite:///database.db

# API Keys
API_KEY=your_api_key_here

# External Services
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
"""
    with open(project_dir / '.env.example', 'w') as f:
        f.write(env_example)

def generate_project_plan(project_data):
    """Generate a detailed project plan based on configuration"""
    logger.info("Starting project plan generation")

    # Basic project info
    title = project_data.get('title') or 'Untitled Project'
    description = project_data.get('description') or 'No description provided'
    project_type = project_data.get('project_type', 'fullstack')
    timeline = project_data.get('timeline', '1week')
    difficulty = project_data.get('difficulty', 'intermediate')
    logger.info(f"Project: {title}, Type: {project_type}, Timeline: {timeline}")

    # Calculate timeline days
    timeline_days = 7
    if timeline == 'weekend':
        timeline_days = 3
    elif timeline == '1week':
        timeline_days = 7
    elif timeline == '2weeks':
        timeline_days = 14
    elif timeline == '1month':
        timeline_days = 30
    elif timeline == '3months':
        timeline_days = 90
    elif timeline == 'open':
        timeline_days = 0
    logger.info(f"Timeline days: {timeline_days}")

    # Tech stack and features
    tech_stack = project_data.get('tech_stack', {})
    features = project_data.get('features', [])
    deployment_platform = project_data.get('deployment_platform', 'github')
    repo_name = project_data.get('repo_name', 'my-project')
    github_username = project_data.get('github_username', 'yourusername')
    include_readme = project_data.get('include_readme', True)
    include_license = project_data.get('include_license', False)
    include_gitignore = project_data.get('include_gitignore', True)
    logger.info(f"Tech stack categories: {list(tech_stack.keys())}, Features count: {len(features)}")

    # Generate components
    try:
        phases = generate_timeline_phases(timeline_days, project_type, difficulty)
        logger.info("Timeline phases generated")
    except Exception as e:
        logger.error(f"Error generating timeline phases: {e}")
        raise

    try:
        file_structure = generate_file_structure(project_type, project_data.get('repo_name', 'my-project'))
        logger.info("File structure generated")
    except Exception as e:
        logger.error(f"Error generating file structure: {e}")
        raise

    try:
        github_username = project_data.get('github_username', 'yourusername')
        repo_name = project_data.get('repo_name', 'my-project')
        getting_started = generate_getting_started(tech_stack, project_type, github_username, repo_name)
        logger.info("Getting started instructions generated")
    except Exception as e:
        logger.error(f"Error generating getting started: {e}")
        raise
    
    plan = f"""# {title}

## 📋 Project Overview
{description}

## 🎯 Project Details
- **Type:** {project_type.replace('_', ' ').title()}
- **Timeline:** {timeline.replace('_', ' ').title()} ({timeline_days} days)
- **Difficulty:** {difficulty.title()}
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🛠️ Tech Stack
### Frontend
{format_tech_list(tech_stack.get('frontend', []))}

### Backend
{format_tech_list(tech_stack.get('backend', []))}

### Database & Storage
{format_tech_list(tech_stack.get('database', []))}

### Tools & DevOps
{format_tech_list(tech_stack.get('tools', []))}

## ✨ Features
{format_features_list(features)}

## 🚀 Deployment
- **Platform:** {deployment_platform.replace('_', ' ').title()}
- **Repository:** https://github.com/{github_username}/{repo_name}
- **Include README:** {'Yes' if include_readme else 'No'}
- **Include License:** {'Yes' if include_license else 'No'}
- **Include .gitignore:** {'Yes' if include_gitignore else 'No'}
- **Include Virtual Environment Setup:** {'Yes' if project_data.get('include_venv', True) else 'No'}

---
*Generated by Vibe Code Assistant on {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    return plan

def format_tech_list(tech_list):
    """Format tech stack list for markdown"""
    if not tech_list:
        return "- *No specific technologies selected*"
    return '\n'.join([f"- {tech}" for tech in tech_list])

def format_features_list(features):
    """Format features list for markdown"""
    if not features:
        return "- *No specific features selected*"
    return '\n'.join([f"- ✅ {feature}" for feature in features])

def generate_timeline_phases(days, project_type, difficulty):
    """Generate development timeline phases"""
    
    if days <= 3:
        phases = [
            ("Planning & Setup", 20, ["Project setup", "Environment configuration", "Basic structure"]),
            ("Core Development", 60, ["Implement main features", "Basic functionality"]),
            ("Testing & Polish", 20, ["Bug fixes", "Basic testing", "Documentation"])
        ]
    elif days <= 7:
        phases = [
            ("Planning & Setup", 15, ["Project setup", "Environment configuration", "Architecture planning"]),
            ("Core Development", 50, ["Database models", "API routes", "Basic UI"]),
            ("Features & Integration", 25, ["Implement features", "Third-party integrations"]),
            ("Testing & Polish", 10, ["Testing", "Bug fixes", "Documentation"])
        ]
    elif days <= 14:
        phases = [
            ("Planning & Setup", 10, ["Project setup", "Environment configuration", "Architecture planning"]),
            ("Core Development", 40, ["Database models", "API routes", "Basic UI"]),
            ("Features & Integration", 35, ["Implement features", "Third-party integrations", "Advanced functionality"]),
            ("Testing & Polish", 15, ["Comprehensive testing", "Bug fixes", "Performance optimization", "Documentation"])
        ]
    else:
        phases = [
            ("Planning & Setup", 10, ["Project setup", "Environment configuration", "Architecture planning", "Team setup"]),
            ("Core Development", 35, ["Database models", "API routes", "Basic UI", "Core features"]),
            ("Features & Integration", 35, ["Implement features", "Third-party integrations", "Advanced functionality", "AI/ML integration"]),
            ("Testing & Polish", 20, ["Comprehensive testing", "Performance optimization", "Security audit", "Documentation", "Deployment"])
        ]
    
    timeline = ""
    current_day = 1
    
    for phase_name, percentage, tasks in phases:
        phase_days = max(1, round(days * percentage / 100))
        end_day = current_day + phase_days - 1
        
        timeline += f"### {phase_name} (Day {current_day}-{end_day})\n"
        for task in tasks:
            timeline += f"- [ ] {task}\n"
        timeline += "\n"
        
        current_day = end_day + 1
    
    return timeline

def generate_file_structure(project_type, repo_name):
    """Generate appropriate file structure based on project type"""
    
    structures = {
        'fullstack': f"""📁 {repo_name}/
├── 📁 frontend/
│   ├── 📄 package.json
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   ├── 📁 pages/
│   │   └── 📁 assets/
│   └── 📄 index.html
├── 📁 backend/
│   ├── 📄 app.py / server.js
│   ├── 📄 requirements.txt / package.json
│   ├── 📁 models/
│   ├── 📁 routes/
│   └── 📁 utils/
├── 📁 database/
│   └── 📄 migrations/
├── 📄 docker-compose.yml
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 README.md
└── 📄 LICENSE""",
        
        'frontend': f"""📁 {repo_name}/
├── 📁 src/
│   ├── 📁 components/
│   ├── 📁 pages/
│   ├── 📁 assets/
│   └── 📁 styles/
├── 📄 package.json
├── 📄 vite.config.js / webpack.config.js
├── 📄 .gitignore
├── 📄 README.md
├── 📄 index.html
└── 📄 LICENSE""",
        
        'backend': f"""📁 {repo_name}/
├── 📁 src/
│   ├── 📁 controllers/
│   ├── 📁 models/
│   ├── 📁 routes/
│   ├── 📁 middleware/
│   └── 📁 utils/
├── 📄 package.json / requirements.txt
├── 📄 server.js / app.py
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 README.md
├── 📄 dockerfile
└── 📄 LICENSE"""
    }
    
    return structures.get(project_type, structures['fullstack'])

def generate_getting_started(tech_stack, project_type, github_username='yourusername', repo_name='my-project'):
    """Generate getting started instructions"""

    frontend = tech_stack.get('frontend', [])
    backend = tech_stack.get('backend', [])

    instructions = "1. Clone the repository:\n"
    instructions += "   ```bash\n"
    instructions += f"   git clone https://github.com/{github_username}/{repo_name}.git\n"
    instructions += f"   cd {repo_name}\n"
    instructions += "   ```\n\n"
    
    if project_type in ['fullstack', 'frontend'] and frontend:
        instructions += "2. Set up frontend:\n"
        instructions += "   ```bash\n"
        if 'React' in frontend:
            instructions += "   cd frontend\n"
            instructions += "   npm install\n"
            instructions += "   npm start\n"
        elif 'Vue.js' in frontend:
            instructions += "   cd frontend\n"
            instructions += "   npm install\n"
            instructions += "   npm run dev\n"
        else:
            instructions += "   # Follow the specific setup instructions for your chosen frontend\n"
        instructions += "   ```\n\n"
    
    if project_type in ['fullstack', 'backend'] and backend:
        instructions += "3. Set up backend:\n"
        instructions += "   ```bash\n"
        if 'Python' in backend or 'Flask' in backend:
            instructions += "   cd backend\n"
            instructions += "   python -m venv venv\n"
            instructions += "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate\n"
            instructions += "   pip install -r requirements.txt\n"
            instructions += "   python app.py\n"
        elif 'Node.js' in backend:
            instructions += "   cd backend\n"
            instructions += "   npm install\n"
            instructions += "   npm start\n"
        else:
            instructions += "   # Follow the specific setup instructions for your chosen backend\n"
        instructions += "   ```\n\n"
    
    instructions += "4. Set up environment variables (copy .env.example to .env)\n"
    instructions += "5. Start development servers\n"
    instructions += "6. Open your browser to the frontend URL\n"
    
    return instructions

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)