
        // Toggle sidebar on mobile
        document.addEventListener('DOMContentLoaded', function() {
            const sidebar = document.querySelector('.sidebar');
            const sidebarToggle = document.querySelector('.sidebar-toggle');
            const sidebarOverlay = document.querySelector('.sidebar-overlay');
            
            // Toggle sidebar when hamburger button is clicked
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('active');
                sidebarOverlay.classList.toggle('active');
            });
            
            // Close sidebar when overlay is clicked
            sidebarOverlay.addEventListener('click', function() {
                sidebar.classList.remove('active');
                sidebarOverlay.classList.remove('active');
            });
            
            // Initialize Bootstrap collapses
            var collapses = document.querySelectorAll('.collapse');
            
            // Make sure dropdowns stay open when clicking inside
            document.querySelectorAll('.dropdown-menu').forEach(function(element) {
                element.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });

            // Get current page URL
            var currentUrl = window.location.href.split('/').pop() || 'index.html';
            
            // Find matching links and add active class
            document.querySelectorAll('.sidebar .nav-link').forEach(link => {
                if (link.getAttribute('href') === currentUrl) {
                    link.classList.add('active');
                    
                    // If it's inside a dropdown, open the dropdown
                    let dropdown = link.closest('.collapse');
                    if (dropdown) {
                        var bsCollapse = new bootstrap.Collapse(dropdown, {
                            toggle: true
                        });
                        
                        let toggle = document.querySelector('[href="#' + dropdown.id + '"]');
                        if (toggle) {
                            toggle.setAttribute('aria-expanded', 'true');
                        }
                    }
                }
            });
        });
   