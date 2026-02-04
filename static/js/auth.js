// MindTrack Authentication JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const container = document.getElementById('container');
    const showSignUp = document.getElementById('showSignUp');
    const showSignIn = document.getElementById('showSignIn');
    const signInOverlay = document.getElementById('signInOverlay');
    const signUpOverlay = document.getElementById('signUpOverlay');
    const signInForm = document.getElementById('signInForm');
    const signUpForm = document.getElementById('signUpForm');
    
    // Password toggle elements
    const toggleSignInPassword = document.getElementById('toggleSignInPassword');
    const toggleSignUpPassword = document.getElementById('toggleSignUpPassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    
    // Form validation elements
    const signInEmail = document.getElementById('id_username');
    const signInPassword = document.getElementById('id_password');
    const signUpEmail = document.getElementById('id_email');
    const signUpPassword = document.getElementById('id_password1');
    const confirmPassword = document.getElementById('id_password2');
    
    // Password strength element
    const passwordStrength = document.getElementById('passwordStrength');
    
    // Event Listeners for panel toggling
    if (showSignUp) {
        showSignUp.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.add('right-panel-active');
        });
    }
    
    if (showSignIn) {
        showSignIn.addEventListener('click', (e) => {
            e.preventDefault();
            container.classList.remove('right-panel-active');
        });
    }
    
    if (signInOverlay) {
        signInOverlay.addEventListener('click', () => {
            container.classList.remove('right-panel-active');
        });
    }
    
    if (signUpOverlay) {
        signUpOverlay.addEventListener('click', () => {
            container.classList.add('right-panel-active');
        });
    }
    
    // Password toggle functionality
    if (toggleSignInPassword) {
        toggleSignInPassword.addEventListener('click', function() {
            togglePasswordVisibility(signInPassword, this);
        });
    }
    
    if (toggleSignUpPassword) {
        toggleSignUpPassword.addEventListener('click', function() {
            togglePasswordVisibility(signUpPassword, this);
        });
    }
    
    if (toggleConfirmPassword) {
        toggleConfirmPassword.addEventListener('click', function() {
            togglePasswordVisibility(confirmPassword, this);
        });
    }
    
    // Real-time validation for sign-up form
    if (signUpPassword) {
        signUpPassword.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });
    }
    
    if (confirmPassword) {
        confirmPassword.addEventListener('input', validateConfirmPassword);
    }
    
    // Functions
    function togglePasswordVisibility(passwordField, toggleButton) {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        
        // Toggle eye icon
        const icon = toggleButton.querySelector('i');
        if (type === 'text') {
            icon.className = '';
            icon.classList.add('far', 'fa-eye-slash');
        } else {
            icon.className = '';
            icon.classList.add('far', 'fa-eye');
        }
    }
    
    function validateConfirmPassword() {
        const password = signUpPassword ? signUpPassword.value : '';
        const confirm = confirmPassword ? confirmPassword.value : '';
        
        if (!confirm) {
            return false;
        }
        
        if (password !== confirm) {
            return false;
        }
        
        return true;
    }
    
    function checkPasswordStrength(password) {
        if (!passwordStrength) return;
        
        let strength = 0;
        
        if (password.length >= 6) strength++;
        if (password.match(/[a-z]+/)) strength++;
        if (password.match(/[A-Z]+/)) strength++;
        if (password.match(/[0-9]+/)) strength++;
        if (password.match(/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/)) strength++;
        
        // Reset classes
        passwordStrength.className = 'password-strength';
        
        if (password.length === 0) {
            return;
        }
        
        if (strength < 2) {
            passwordStrength.classList.add('password-weak');
        } else if (strength < 4) {
            passwordStrength.classList.add('password-medium');
        } else {
            passwordStrength.classList.add('password-strong');
        }
    }
    
    // Show loading state on form submission
    if (signInForm) {
        signInForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.classList.add('loading');
        });
    }
    
    if (signUpForm) {
        signUpForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.classList.add('loading');
        });
    }
    
    // Terms and Privacy modals
    window.showTerms = function() {
        alert('MindTrack Terms of Service:\n\n1. You agree to use this service responsibly\n2. Your data will be stored for 1 week\n3. Free tier includes 3 mood analyses\n4. Premium features require subscription');
        return false;
    }
    
    window.showPrivacy = function() {
        alert('MindTrack Privacy Policy:\n\n1. We respect your privacy\n2. Mood data is confidential\n3. No data sharing with third parties\n4. Data auto-deleted after 1 week\n5. You can delete your account anytime');
        return false;
    }
    
    // Auto-switch to sign-in if there are sign-in errors
    const signInErrors = document.querySelectorAll('#signInForm .error-message');
    if (signInErrors.length > 0) {
        container.classList.remove('right-panel-active');
    }
    
    // Auto-switch to sign-up if there are sign-up errors
    const signUpErrors = document.querySelectorAll('#signUpForm .error-message');
    if (signUpErrors.length > 0) {
        container.classList.add('right-panel-active');
    }
});