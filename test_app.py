#!/usr/bin/env python3
"""
Unit tests for Vibe Coding Generator
Basic test suite to ensure core functionality works correctly
"""

import pytest
import json
from app import app, db, Project, validate_project_data, generate_project_plan

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        'title': 'Test Project',
        'description': 'A test project for unit testing',
        'project_type': 'fullstack',
        'timeline': '1week',
        'difficulty': 'intermediate',
        'tech_stack': {
            'frontend': ['React'],
            'backend': ['Python'],
            'database': ['SQLite'],
            'tools': ['Git']
        },
        'features': ['Authentication', 'CRUD Operations'],
        'deployment_platform': 'github',
        'repo_name': 'test-project',
        'include_readme': True,
        'include_license': False,
        'include_gitignore': True
    }

class TestProjectValidation:
    """Test project data validation"""
    
    def test_valid_project_data(self):
        """Test that valid project data passes validation"""
        data = {
            'project_type': 'fullstack',
            'timeline': '1week',
            'difficulty': 'intermediate'
        }
        is_valid, error_msg = validate_project_data(data)
        assert is_valid is True
        assert error_msg is None
    
    def test_missing_required_fields(self):
        """Test that missing required fields fail validation"""
        data = {
            'project_type': 'fullstack',
            'timeline': '1week'
            # missing 'difficulty'
        }
        is_valid, error_msg = validate_project_data(data)
        assert is_valid is False
        assert 'Missing required field: difficulty' in error_msg
    
    def test_invalid_project_type(self):
        """Test that invalid project type fails validation"""
        data = {
            'project_type': 'invalid_type',
            'timeline': '1week',
            'difficulty': 'intermediate'
        }
        is_valid, error_msg = validate_project_data(data)
        assert is_valid is False
        assert 'Invalid project type' in error_msg
    
    def test_invalid_timeline(self):
        """Test that invalid timeline fails validation"""
        data = {
            'project_type': 'fullstack',
            'timeline': 'invalid_timeline',
            'difficulty': 'intermediate'
        }
        is_valid, error_msg = validate_project_data(data)
        assert is_valid is False
        assert 'Invalid timeline' in error_msg
    
    def test_invalid_difficulty(self):
        """Test that invalid difficulty fails validation"""
        data = {
            'project_type': 'fullstack',
            'timeline': '1week',
            'difficulty': 'invalid_difficulty'
        }
        is_valid, error_msg = validate_project_data(data)
        assert is_valid is False
        assert 'Invalid difficulty' in error_msg

class TestProjectPlanGeneration:
    """Test project plan generation"""
    
    def test_generate_basic_plan(self):
        """Test generating a basic project plan"""
        data = {
            'title': 'Test Project',
            'description': 'A test project',
            'project_type': 'frontend',
            'timeline': '1week',
            'difficulty': 'beginner',
            'tech_stack': {
                'frontend': ['React'],
                'backend': [],
                'database': [],
                'tools': []
            },
            'features': ['Authentication'],
            'repo_name': 'test-project'
        }
        
        plan = generate_project_plan(data)
        
        # Check that plan contains expected sections
        assert 'Test Project' in plan
        assert 'A test project' in plan
        assert 'Frontend' in plan
        assert 'React' in plan
        assert 'Authentication' in plan
        assert '📅 Development Timeline' in plan
        assert '🚀 Getting Started' in plan
    
    def test_generate_plan_with_empty_fields(self):
        """Test generating plan with empty title and description"""
        data = {
            'title': '',
            'description': '',
            'project_type': 'backend',
            'timeline': '2weeks',
            'difficulty': 'advanced',
            'tech_stack': {
                'frontend': [],
                'backend': ['Python', 'Flask'],
                'database': ['PostgreSQL'],
                'tools': ['Docker']
            },
            'features': ['API Integration'],
            'repo_name': 'empty-project'
        }
        
        plan = generate_project_plan(data)
        
        # Should handle empty fields gracefully
        assert 'Untitled Project' in plan
        assert 'No description provided' in plan
        assert 'Backend' in plan
        assert 'Python' in plan
        assert 'Flask' in plan

class TestFlaskRoutes:
    """Test Flask application routes"""
    
    def test_index_route(self, client):
        """Test that the index route loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Vibe Coding Generator' in response.data
    
    def test_tech_stacks_api(self, client):
        """Test the tech stacks API endpoint"""
        response = client.get('/api/tech-stacks')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'frontend' in data
        assert 'backend' in data
        assert 'database' in data
        assert 'tools' in data
        assert isinstance(data['frontend'], list)
    
    def test_features_api(self, client):
        """Test the features API endpoint"""
        response = client.get('/api/features')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_create_project_success(self, client, sample_project_data):
        """Test successful project creation"""
        response = client.post('/api/projects',
                             json=sample_project_data,
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'project' in data
        assert data['project']['title'] == 'Test Project'
        assert data['project']['project_type'] == 'fullstack'
    
    def test_create_project_validation_error(self, client):
        """Test project creation with invalid data"""
        invalid_data = {
            'title': 'Test Project'
            # missing required fields
        }
        
        response = client.post('/api/projects',
                             json=invalid_data,
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_generate_project_plan(self, client, sample_project_data):
        """Test project plan generation endpoint"""
        response = client.post('/api/generate',
                             json={'project': sample_project_data},
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'plan' in data
        assert 'Test Project' in data['plan']

class TestDatabaseOperations:
    """Test database operations"""
    
    def test_create_project_in_database(self, client, sample_project_data):
        """Test creating a project in the database"""
        # Create project
        response = client.post('/api/projects',
                             json=sample_project_data,
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        project_id = data['project']['id']
        
        # Retrieve project
        response = client.get(f'/api/projects/{project_id}')
        assert response.status_code == 200
        
        retrieved_data = json.loads(response.data)
        assert retrieved_data['title'] == 'Test Project'
        assert retrieved_data['project_type'] == 'fullstack'
    
    def test_get_all_projects(self, client, sample_project_data):
        """Test retrieving all projects"""
        # Create a project
        client.post('/api/projects',
                   json=sample_project_data,
                   content_type='application/json')
        
        # Get all projects
        response = client.get('/api/projects')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0

if __name__ == '__main__':
    # Run tests if script is executed directly
    pytest.main([__file__, '-v'])