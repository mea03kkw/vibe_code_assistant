/**
 * Vibe Coding Generator - Demo JavaScript Application
 * Static demo version with hardcoded data and local generation
 */

// Global variables
let techStacks = {};
let availableFeatures = [];
let selectedTechStack = {
    frontend: new Set(),
    backend: new Set(),
    database: new Set(),
    tools: new Set()
};
let selectedFeatures = new Set();
let customFeatures = [];

// Tech stack icons mapping
const techIcons = {
    // Frontend
    'React': 'bi-code-slash',
    'Vue.js': 'bi-code-slash',
    'Angular': 'bi-code-slash',
    'Svelte': 'bi-code-slash',
    'Next.js': 'bi-code-slash',
    'Nuxt.js': 'bi-code-slash',
    'HTML/CSS/JS': 'bi-file-earmark-code',
    'TypeScript': 'bi-filetype-ts',
    'Tailwind CSS': 'bi-palette',
    'Bootstrap': 'bi-bootstrap',
    'Material UI': 'bi-palette',

    // Backend
    'Node.js': 'bi-node-plus',
    'Express': 'bi-server',
    'Python': 'bi-code-slash',
    'Flask': 'bi-server',
    'Django': 'bi-server',
    'FastAPI': 'bi-server',
    'Ruby on Rails': 'bi-gem',
    'Spring Boot': 'bi-cpu',
    'Laravel': 'bi-server',
    'ASP.NET': 'bi-windows',
    'Go': 'bi-code-slash',
    'Rust': 'bi-gear',

    // Database
    'PostgreSQL': 'bi-database',
    'MySQL': 'bi-database',
    'MongoDB': 'bi-database',
    'SQLite': 'bi-database',
    'Redis': 'bi-database',
    'Firebase': 'bi-cloud',
    'Supabase': 'bi-database',
    'GraphQL': 'bi-diagram-3',
    'Elasticsearch': 'bi-search',

    // Tools
    'Docker': 'bi-box-seam',
    'Git': 'bi-git',
    'GitHub Actions': 'bi-github',
    'Jest': 'bi-check-circle',
    'Cypress': 'bi-check-circle',
    'Webpack': 'bi-gear',
    'Vite': 'bi-gear',
    'Ollama': 'bi-robot',
    'OpenAI API': 'bi-robot'
};

// Feature icons mapping
const featureIcons = {
    'Authentication (OAuth, JWT, sessions)': 'bi-shield-lock',
    'Admin Panel': 'bi-person-gear',
    'AI Integration (ChatGPT, local models)': 'bi-robot',
    'Real-time features (WebSockets)': 'bi-lightning',
    'CRUD Operations': 'bi-database-add',
    'Analytics & Statistics': 'bi-graph-up',
    'File Upload': 'bi-cloud-upload',
    'Payment Integration': 'bi-credit-card'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    try {
        // Load tech stacks and features (hardcoded for demo)
        loadTechStacks();
        loadFeatures();

        // Initialize UI components
        initializeTechStacks();
        initializeFeatures();
        initializeEventListeners();

        // Set up default selections
        setupDefaultSelections();

        console.log('Vibe Code Assistant Demo initialized successfully');
    } catch (error) {
        console.error('Failed to initialize demo app:', error);
        showAlert('Failed to load demo application data. Please refresh the page.', 'danger');
    }
}

function loadTechStacks() {
    // Hardcoded tech stacks for demo
    techStacks = {
        frontend: ['React', 'Vue.js', 'Angular', 'Svelte', 'Next.js', 'HTML/CSS/JS', 'TypeScript', 'Tailwind CSS', 'Bootstrap', 'Material UI'],
        backend: ['Node.js', 'Express', 'Python', 'Flask', 'Django', 'FastAPI', 'Ruby on Rails', 'Spring Boot', 'Laravel', 'Go', 'Rust'],
        database: ['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite', 'Redis', 'Firebase', 'Supabase', 'GraphQL', 'Elasticsearch'],
        tools: ['Docker', 'Git', 'GitHub Actions', 'Jest', 'Cypress', 'Webpack', 'Vite', 'Ollama', 'OpenAI API']
    };
    console.log('Tech stacks loaded (demo):', techStacks);
}

function loadFeatures() {
    // Hardcoded features for demo
    availableFeatures = [
        'Authentication (OAuth, JWT, sessions)',
        'Admin Panel',
        'AI Integration (ChatGPT, local models)',
        'Real-time features (WebSockets)',
        'CRUD Operations',
        'Analytics & Statistics',
        'File Upload',
        'Payment Integration'
    ];
    console.log('Features loaded (demo):', availableFeatures);
}

function initializeTechStacks() {
    // Populate tech stack containers with card-style checkboxes
    for (const category in techStacks) {
        const container = document.getElementById(category + 'Stack');
        if (container) {
            container.innerHTML = '';

            techStacks[category].forEach(tech => {
                const techId = `${category}_${tech.replace(/\s+/g, '_').toLowerCase()}`;

                const techDiv = document.createElement('div');
                techDiv.className = 'col-4 col-sm-3 col-md-3 col-lg-2';

                const iconClass = techIcons[tech] || 'bi-code-slash';

                techDiv.innerHTML = `
                    <div class="card h-100 tech-card">
                        <div class="card-body text-center d-flex flex-column align-items-center justify-content-center">
                            <i class="bi ${iconClass} tech-icon mb-1" style="font-size: 1.2rem;"></i>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="${techId}"
                                       value="${tech}" onchange="updateTechSelection('${category}', '${tech}', this.checked)">
                                <label class="form-check-label w-100" for="${techId}">
                                    <h6 class="card-title mb-0">${tech}</h6>
                                </label>
                            </div>
                        </div>
                    </div>
                `;

                container.appendChild(techDiv);
            });
        }
    }
}

function initializeFeatures() {
    const container = document.getElementById('featuresContainer');
    if (container) {
        container.innerHTML = '';

        availableFeatures.forEach((feature, index) => {
            const featureId = `feature_${index}`;

            const featureDiv = document.createElement('div');
            featureDiv.className = 'col-4 col-sm-3 col-md-3';

            const iconClass = featureIcons[feature] || 'bi-star';

            featureDiv.innerHTML = `
                <div class="card h-100 feature-card">
                    <div class="card-body text-center d-flex flex-column align-items-center justify-content-center">
                        <i class="bi ${iconClass} feature-icon mb-1" style="font-size: 1.2rem;"></i>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="${featureId}"
                                   value="${feature}" onchange="updateFeatureSelection('${feature}', this.checked)">
                            <label class="form-check-label w-100" for="${featureId}">
                                <h6 class="card-title mb-0">${feature}</h6>
                            </label>
                        </div>
                    </div>
                </div>
            `;

            container.appendChild(featureDiv);
        });
    }
}

function initializeEventListeners() {
    // No preview listeners needed
}

function setupDefaultSelections() {
    // Set some default tech stack selections
    updateTechSelection('frontend', 'React', true);
    updateTechSelection('backend', 'Python', true);
    updateTechSelection('database', 'SQLite', true);
    updateTechSelection('tools', 'Git', true);

    // Set some default features
    updateFeatureSelection('Authentication (OAuth, JWT, sessions)', true);
    updateFeatureSelection('CRUD Operations', true);
    updateFeatureSelection('AI Integration (ChatGPT, local models)', true);
}

function updateTechSelection(category, tech, checked) {
    if (checked) {
        selectedTechStack[category].add(tech);
    } else {
        selectedTechStack[category].delete(tech);
    }
}

function updateFeatureSelection(feature, checked) {
    if (checked) {
        selectedFeatures.add(feature);
    } else {
        selectedFeatures.delete(feature);
    }
}

function addTech(category) {
    const inputId = 'new' + category.charAt(0).toUpperCase() + category.slice(1) + 'Tech';
    const input = document.getElementById(inputId);
    const techName = input.value.trim();

    if (techName) {
        // Add to selected tech stack
        selectedTechStack[category].add(techName);

        // Add card to the UI
        const container = document.getElementById(category + 'Stack');
        const techId = `${category}_${techName.replace(/\s+/g, '_').toLowerCase()}`;

        const iconClass = techIcons[techName] || 'bi-code-slash';

        const techDiv = document.createElement('div');
        techDiv.className = 'col-4 col-sm-3 col-md-3 col-lg-2';

        techDiv.innerHTML = `
            <div class="card h-100 tech-card">
                <div class="card-body text-center d-flex flex-column align-items-center justify-content-center">
                    <i class="bi ${iconClass} tech-icon mb-1" style="font-size: 1.2rem;"></i>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="${techId}"
                               value="${techName}" checked onchange="updateTechSelection('${category}', '${techName}', this.checked)">
                        <label class="form-check-label w-100" for="${techId}">
                            <h6 class="card-title mb-0">${techName} <span class="badge bg-info ms-1">Custom</span></h6>
                        </label>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(techDiv);

        // Clear input
        input.value = '';

        showAlert(`Added ${techName} to ${category} technologies`, 'success');
    }
}

function addCustomFeature() {
    const input = document.getElementById('customFeature');
    const featureName = input.value.trim();

    if (featureName) {
        // Add to custom features
        customFeatures.push(featureName);
        selectedFeatures.add(featureName);

        // Add to UI
        const container = document.getElementById('customFeaturesList');
        const badge = document.createElement('span');
        badge.className = 'badge bg-warning text-dark me-1 mb-1';
        badge.textContent = featureName;
        container.appendChild(badge);

        // Clear input
        input.value = '';

        showAlert(`Added custom feature: ${featureName}`, 'success');
    }
}

async function generateProject() {
    try {
        showLoading(true);

        // Collect form data
        const titleValue = document.getElementById('projectTitle').value.trim();
        const descriptionValue = document.getElementById('projectDescription').value.trim();

        // Calculate timeline days
        const timelineValue = document.getElementById('timelineSelect').value;
        let timelineDays = 7;
        switch(timelineValue) {
            case 'weekend': timelineDays = 3; break;
            case '1week': timelineDays = 7; break;
            case '2weeks': timelineDays = 14; break;
            case '1month': timelineDays = 30; break;
            case '3months': timelineDays = 90; break;
            case 'open': timelineDays = 0; break;
        }

        const projectData = {
            title: titleValue || 'Demo Project',
            description: descriptionValue || 'A demo project generated by Vibe Code Assistant',
            project_type: document.querySelector('input[name="projectType"]:checked').id,
            timeline: timelineValue,
            timeline_days: timelineDays,
            difficulty: document.getElementById('difficultySelect').value,
            tech_stack: {
                frontend: Array.from(selectedTechStack.frontend),
                backend: Array.from(selectedTechStack.backend),
                database: Array.from(selectedTechStack.database),
                tools: Array.from(selectedTechStack.tools)
            },
            features: Array.from(selectedFeatures),
            deployment_platform: document.getElementById('deploymentPlatform').value,
            repo_name: document.getElementById('repoName').value || (titleValue || 'demo-project').toLowerCase().replace(/\s+/g, '-'),
            github_username: document.getElementById('githubUsername').value.trim() || 'demo-user',
            include_readme: document.getElementById('includeReadme').checked,
            include_license: document.getElementById('includeLicense').checked,
            include_gitignore: document.getElementById('includeGitignore').checked
        };

        // Generate demo project plan
        const plan = generateDemoProjectPlan(projectData);

        // Display generated project plan
        document.getElementById('generatedOutput').innerHTML =
            `<div class="mb-0" style="white-space: pre-wrap; font-family: monospace; word-wrap: break-word;">${plan}</div>`;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('projectModal'));
        modal.show();

        showAlert('Demo project plan generated successfully!', 'success');

    } catch (error) {
        console.error('Error generating demo project:', error);
        showAlert('Failed to generate demo project plan. Please try again.', 'danger');
    } finally {
        showLoading(false);
    }
}

function generateDemoProjectPlan(projectData) {
    const title = projectData.title;
    const description = projectData.description;
    const projectType = projectData.project_type.replace('Only', '').toLowerCase();
    const timeline = projectData.timeline;
    const difficulty = projectData.difficulty;
    const techStack = projectData.tech_stack;
    const features = projectData.features;
    const deployment = projectData.deployment_platform;
    const repoName = projectData.repo_name;
    const username = projectData.github_username;

    // Calculate timeline days
    let days = 7;
    switch(timeline) {
        case 'weekend': days = 3; break;
        case '1week': days = 7; break;
        case '2weeks': days = 14; break;
        case '1month': days = 30; break;
        case '3months': days = 90; break;
        case 'open': days = 0; break;
    }

    const plan = `# ${title}

## 📋 Project Overview
${description}

## 🎯 Project Details
- **Type:** ${projectType.charAt(0).toUpperCase() + projectType.slice(1)}
- **Timeline:** ${timeline.replace(/(\d+)/, '$1 ')} (${days} days)
- **Difficulty:** ${difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
- **Created:** ${new Date().toLocaleDateString()}

## 🛠️ Tech Stack
### Frontend
${techStack.frontend.map(tech => `- ${tech}`).join('\n') || '- No frontend technologies selected'}

### Backend
${techStack.backend.map(tech => `- ${tech}`).join('\n') || '- No backend technologies selected'}

### Database & Storage
${techStack.database.map(tech => `- ${tech}`).join('\n') || '- No database technologies selected'}

### Tools & DevOps
${techStack.tools.map(tech => `- ${tech}`).join('\n') || '- No tools selected'}

## ✨ Features
${features.map(feature => `- ✅ ${feature}`).join('\n') || '- No features selected'}

## 🚀 Deployment
- **Platform:** ${deployment.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
- **Repository:** https://github.com/${username}/${repoName}

---

*Generated by Vibe Code Assistant Demo on ${new Date().toLocaleDateString()}*
`;

    return plan;
}

function copyProjectToClipboard() {
    const text = document.querySelector('#generatedOutput > *').textContent;

    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Demo project plan copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();

    try {
        document.execCommand('copy');
        showAlert('Demo project plan copied to clipboard!', 'success');
    } catch (err) {
        showAlert('Failed to copy to clipboard', 'danger');
    }

    document.body.removeChild(textArea);
}

async function downloadProjectFiles() {
    showAlert('Download feature not available in demo mode. Please use the full application for file downloads.', 'info');
}

function saveConfiguration() {
    const config = {
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value,
        tech_stack: {
            frontend: Array.from(selectedTechStack.frontend),
            backend: Array.from(selectedTechStack.backend),
            database: Array.from(selectedTechStack.database),
            tools: Array.from(selectedTechStack.tools)
        },
        features: Array.from(selectedFeatures),
        custom_features: customFeatures,
        timestamp: new Date().toISOString()
    };

    try {
        localStorage.setItem('vibeCodingDemoConfig', JSON.stringify(config));
        showAlert('Demo configuration saved locally!', 'success');
    } catch (error) {
        console.error('Error saving demo configuration:', error);
        showAlert('Failed to save demo configuration', 'danger');
    }
}

function loadSampleConfig() {
    const sampleConfig = {
        title: "E-commerce Platform with AI Recommendations",
        description: "A modern e-commerce platform with AI-powered product recommendations, real-time inventory management, and seamless checkout experience with advanced analytics.",
        tech_stack: {
            frontend: ["Next.js", "TypeScript", "Tailwind CSS"],
            backend: ["Node.js", "Express", "MongoDB"],
            database: ["MongoDB", "Redis"],
            tools: ["Docker", "Jest", "GitHub Actions", "Stripe API"]
        },
        features: ["Authentication", "Payment Integration", "AI Integration", "Real-time Features", "Admin Panel", "Analytics & Stats"]
    };

    // Apply sample config
    document.getElementById('projectTitle').value = sampleConfig.title;
    document.getElementById('projectDescription').value = sampleConfig.description;

    // Clear current selections
    for (const category in selectedTechStack) {
        selectedTechStack[category].clear();
    }
    selectedFeatures.clear();
    customFeatures = [];

    // Set sample selections
    for (const category in sampleConfig.tech_stack) {
        sampleConfig.tech_stack[category].forEach(tech => {
            selectedTechStack[category].add(tech);
        });
    }

    sampleConfig.features.forEach(feature => {
        selectedFeatures.add(feature);
    });

    // Update UI checkboxes
    updateTechStackCheckboxes();
    updateFeatureCheckboxes();

    // Clear custom features list
    document.getElementById('customFeaturesList').innerHTML = '';

    showAlert('Demo sample configuration loaded!', 'success');
}

function updateTechStackCheckboxes() {
    // Uncheck all checkboxes first
    document.querySelectorAll('input[type="checkbox"][id*="_"]').forEach(checkbox => {
        checkbox.checked = false;
    });

    // Check selected tech stack items
    for (const category in selectedTechStack) {
        selectedTechStack[category].forEach(tech => {
            const checkboxId = `${category}_${tech.replace(/\s+/g, '_').toLowerCase()}`;
            const checkbox = document.getElementById(checkboxId);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
    }
}

function updateFeatureCheckboxes() {
    // Uncheck all feature checkboxes
    document.querySelectorAll('#featuresContainer input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });

    // Check selected features
    selectedFeatures.forEach(feature => {
        const checkbox = Array.from(document.querySelectorAll('#featuresContainer input[type="checkbox"]'))
            .find(cb => cb.value === feature);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
}

function exportConfig() {
    const config = {
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value,
        project_type: document.querySelector('input[name="projectType"]:checked')?.id || 'fullStack',
        timeline: document.getElementById('timelineSelect').value,
        difficulty: document.getElementById('difficultySelect').value,
        tech_stack: {
            frontend: Array.from(selectedTechStack.frontend),
            backend: Array.from(selectedTechStack.backend),
            database: Array.from(selectedTechStack.database),
            tools: Array.from(selectedTechStack.tools)
        },
        features: Array.from(selectedFeatures),
        custom_features: customFeatures,
        deployment_platform: document.getElementById('deploymentPlatform').value,
        repo_name: document.getElementById('repoName').value,
        github_username: document.getElementById('githubUsername').value.trim(),
        include_readme: document.getElementById('includeReadme').checked,
        include_license: document.getElementById('includeLicense').checked,
        include_gitignore: document.getElementById('includeGitignore').checked,
        timestamp: new Date().toISOString()
    };

    const dataStr = JSON.stringify(config, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);

    const exportFileDefaultName = 'vibe-coding-demo-config.json';

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();

    showAlert('Demo configuration exported as JSON file!', 'success');
}

function resetConfiguration() {
    if (confirm('Are you sure you want to reset all demo settings?')) {
        // Reset form
        document.getElementById('projectTitle').value = '';
        document.getElementById('projectDescription').value = '';
        document.getElementById('fullStack').checked = true;
        document.getElementById('timelineSelect').selectedIndex = 1;
        document.getElementById('difficultySelect').selectedIndex = 1;

        // Reset deployment settings
        document.getElementById('deploymentPlatform').selectedIndex = 0;
        document.getElementById('repoName').value = '';
        document.getElementById('includeReadme').checked = true;
        document.getElementById('includeLicense').checked = false;
        document.getElementById('includeGitignore').checked = true;

        // Reset tech stacks and features
        for (const category in selectedTechStack) {
            selectedTechStack[category].clear();
        }
        selectedFeatures.clear();
        customFeatures = [];

        // Reset UI
        updateTechStackCheckboxes();
        updateFeatureCheckboxes();
        document.getElementById('customFeaturesList').innerHTML = '';

        showAlert('Demo configuration reset!', 'info');
    }
}

function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.classList.remove('d-none');
    } else {
        spinner.classList.add('d-none');
    }
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Add to page
    document.body.appendChild(alertDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Initialize demo app when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp);