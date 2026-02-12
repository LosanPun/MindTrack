// Theme Management
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Set initial theme
        this.setTheme(this.theme);

        // Create theme toggle button
        this.createToggleButton();

        // Listen for system theme changes
        this.listenForSystemTheme();
    }

    setTheme(theme) {
        console.log('Setting theme to:', theme);
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);

        // Store theme in session via AJAX
        fetch('/accounts/set-theme/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
            },
            body: JSON.stringify({ theme: theme })
        }).then(response => {
            if (!response.ok) {
                console.error('Failed to save theme to session');
            }
        }).catch(error => {
            console.error('Error saving theme:', error);
        });

        // Update toggle button icon
        this.updateToggleIcon();
    }

    toggleTheme() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    createToggleButton() {
        // Find the dashboard header
        const header = document.querySelector('.dashboard-header');
        if (!header) {
            console.error('Dashboard header not found');
            return;
        }

        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'theme-toggle';
        toggleBtn.setAttribute('aria-label', 'Toggle theme');
        toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
        toggleBtn.style.cssText = `
            background: linear-gradient(135deg, #d4af37, #f4e4a6);
            border: 2px solid rgba(212, 175, 55, 0.3);
            color: #0a1931;
            font-size: 18px;
            cursor: pointer;
            padding: 12px;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin-right: 15px;
        `;

        // Add click event
        toggleBtn.addEventListener('click', (e) => {
            console.log('Theme toggle clicked');
            e.preventDefault();
            this.toggleTheme();
        });

        // Insert before user actions
        const userActions = header.querySelector('.user-actions');
        if (userActions) {
            userActions.insertBefore(toggleBtn, userActions.firstChild);
            console.log('Theme toggle button inserted before user actions');
        } else {
            header.appendChild(toggleBtn);
            console.log('Theme toggle button appended to header');
        }

        this.toggleBtn = toggleBtn;
        this.updateToggleIcon();
        console.log('Theme toggle button created and initialized');
    }

    updateToggleIcon() {
        if (!this.toggleBtn) return;

        const icon = this.toggleBtn.querySelector('i');
        if (this.theme === 'light') {
            icon.className = 'fas fa-moon';
            this.toggleBtn.setAttribute('aria-label', 'Switch to dark theme');
            this.toggleBtn.classList.remove('dark-mode');
        } else {
            icon.className = 'fas fa-sun';
            this.toggleBtn.setAttribute('aria-label', 'Switch to light theme');
            this.toggleBtn.classList.add('dark-mode');
        }
    }

    listenForSystemTheme() {
        // Listen for system theme changes (if user hasn't set preference)
        if (!localStorage.getItem('theme')) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                const newTheme = e.matches ? 'dark' : 'light';
                this.setTheme(newTheme);
            });
        }
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
});

// Export for potential use in other scripts
window.ThemeManager = ThemeManager;
