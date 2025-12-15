# Vibe Coding Generator - Custom Project Builder

[![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://mea03kkw.github.io/vibe_code_assistant/demo.html)

A Flask-based web application for generating customized development project plans with flexible tech stack selection, timeline planning, and feature configuration.

## 🎯 Features

- **Complete Customization**: Define project title, description, and type
- **Flexible Timeline**: Choose from preset options or set custom duration (1-90 days)
- **Tech Stack Freedom**: Select from extensive technology categories:
  - Frontend (React, Vue.js, Angular, Svelte, etc.)
  - Backend (Node.js, Python, Flask, Django, etc.)
  - Database (PostgreSQL, MongoDB, SQLite, Redis, etc.)
  - Tools (Docker, Git, CI/CD, Testing frameworks)
- **Feature Selection**: Choose from pre-built features or add custom ones
- **Real-time Preview**: Live updates as you configure your project
- **Project Generation**: Creates detailed project plans with timeline and file structure
- **Bootstrap-only Design**: Clean, responsive interface using Bootstrap 5
- **Mobile Responsive**: Works perfectly on all device sizes

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vibe-code-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
vibe-code-assistant/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    └── js/
        └── app.js        # Client-side JavaScript
```

## 🛠️ Tech Stack

- **Backend**: Python Flask + SQLAlchemy + SQLite
- **Frontend**: HTML5 + Bootstrap 5 + Vanilla JavaScript
- **Database**: SQLite (for project persistence)
- **Deployment**: GitHub Pages compatible

## 🎮 How to Use

1. **Project Brief**: Enter your project title and detailed description
2. **Project Type**: Choose Full Stack, Frontend Only, or Backend Only
3. **Timeline**: Select completion timeframe (weekend to 3+ months) or set custom days
4. **Difficulty**: Pick your skill level (Beginner to Expert)
5. **Tech Stack**: Select technologies from each category or add custom ones
6. **Features**: Choose from pre-built features or add custom requirements
7. **Preview**: Watch real-time updates in the preview panel
8. **Generate**: Create your detailed project plan with timeline and file structure

## 💡 Key Features Explained

### Tech Stack Selection
- **Frontend**: Modern frameworks and libraries for user interfaces
- **Backend**: Server-side technologies for API and business logic
- **Database**: Data storage solutions from relational to NoSQL
- **Tools**: Development tools, testing frameworks, and DevOps

### Timeline Planning
- **Weekend Project**: 2-3 days for quick prototypes
- **1 Week Challenge**: Sprint-style development
- **2 Weeks Sprint**: Medium complexity projects
- **1 Month Project**: Comprehensive applications
- **3 Months**: Learning-focused projects
- **Custom**: Set any duration from 1-90 days

### Project Generation
The generator creates detailed project plans including:
- Project overview and specifications
- Complete tech stack documentation
- File structure visualization
- Development timeline with phases
- Getting started guide
- Next steps checklist

## 🔧 Development

### Adding New Technologies
Edit the `DEFAULT_TECH_STACKS` in `app.py`:

```python
DEFAULT_TECH_STACKS = {
    'frontend': ['React', 'Vue.js', 'YourNewTech'],
    'backend': ['Node.js', 'Python', 'YourNewBackend'],
    # ... add more categories
}
```

### Adding New Features
Update the `DEFAULT_FEATURES` list in `app.py`:

```python
DEFAULT_FEATURES = [
    'Existing Feature',
    'Your New Feature',
    # ... add more
]
```

## 🌐 Deployment

### GitHub Pages
This application is designed to be deployed on GitHub Pages with Flask integration.

**Live Demo**: [https://mea03kkw.github.io/vibe_code_assistant/demo.html](https://mea03kkw.github.io/vibe_code_assistant/demo.html)

### Local Development
```bash
python app.py
# Visit http://localhost:5000
```

### Production Deployment
For production deployment, consider:
- Using a proper WSGI server (Gunicorn)
- Setting environment variables for security
- Configuring a proper database (PostgreSQL)
- Using a CDN for static assets

## 📱 Mobile Support

The application is fully responsive and works great on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the console for error messages
2. Ensure all dependencies are installed correctly
3. Verify Python version compatibility
4. Check that port 5000 is available

## 🔮 Future Enhancements

- [ ] User authentication and project sharing
- [ ] More deployment platform options
- [ ] Advanced project templates
- [ ] Collaboration features
- [ ] Integration with version control systems
- [ ] Advanced analytics and reporting
- [ ] Plugin system for custom generators

---

**Built with ❤️ using Python Flask and Bootstrap 5**