   // Theme Toggle Functionality
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const themeName = document.getElementById('themeName');
        const html = document.documentElement;
        
        // Check for saved theme or prefer-color-scheme
        const savedTheme = localStorage.getItem('theme') || 
                          (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        
        html.setAttribute('data-theme', savedTheme);
        updateThemeUI(savedTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeUI(newTheme);
            
            // Add animation
            themeToggle.style.transform = 'rotate(360deg) scale(1.1)';
            setTimeout(() => {
                themeToggle.style.transform = '';
            }, 300);
        });
        
        function updateThemeUI(theme) {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-sun';
                themeName.textContent = 'Dark Mode';
            } else {
                themeIcon.className = 'fas fa-moon';
                themeName.textContent = 'Light Mode';
            }
        }
        
        // Mobile menu toggle
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        const sidebar = document.getElementById('sidebar');
        
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', () => {
                sidebar.classList.toggle('active');
            });
            
            // Close sidebar when clicking outside on mobile
            document.addEventListener('click', (event) => {
                if (window.innerWidth <= 992 && 
                    !sidebar.contains(event.target) && 
                    !mobileMenuToggle.contains(event.target)) {
                    sidebar.classList.remove('active');
                }
            });
        }
        
        // Smooth transitions for theme change
        const style = document.createElement('style');
        style.textContent = `
            * {
                transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
            }
        `;
        document.head.appendChild(style);


       