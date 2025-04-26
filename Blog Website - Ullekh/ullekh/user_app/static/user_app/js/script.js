// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Signup/signin input handling
    const inputs = document.querySelectorAll('.input-group input');

    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.closest('.input-group').classList.add('active');
        });

        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.closest('.input-group').classList.remove('active');
            }
        });

        // Check if the input has a value on page load
        if (input.value !== '') {
            input.closest('.input-group').classList.add('active');
        }
    });

    // Account page navigation
    const navLinks = document.querySelectorAll('.profile-nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

    function showTab(tabId) {
        tabContents.forEach(content => {
            if (content.id === tabId) {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
        
        navLinks.forEach(link => {
            if (link.getAttribute('data-tab') === tabId) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tabId = this.getAttribute('data-tab');
            showTab(tabId);
            history.pushState(null, '', `?tab=${tabId}`);
        });
    });

    // Handle back/forward browser navigation
    window.addEventListener('popstate', function() {
        const tabId = new URLSearchParams(window.location.search).get('tab') || 'about';
        showTab(tabId);
    });

    // Show initial tab on account page
    if (document.querySelector('.profile-nav-link')) {
        const initialTab = new URLSearchParams(window.location.search).get('tab') || 'about';
        showTab(initialTab);
    }
});