document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
    const sidebar = document.querySelector('.sidebar');
    const contentWrapper = document.querySelector('.content-wrapper');
    const navbar = document.querySelector('.navbar');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    
    console.log('Sidebar toggle button:', sidebarToggle);
    
    
    function checkSidebarState() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            navbar.classList.add('sidebar-collapsed');
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
        } else {
            const sidebarOpen = localStorage.getItem('sidebarOpen');
            
            if (sidebarOpen === 'false') {
                sidebar.classList.add('collapsed');
                contentWrapper.classList.add('expanded');
                navbar.classList.add('sidebar-collapsed');
            } else {
                sidebar.classList.remove('collapsed');
                contentWrapper.classList.remove('expanded');
                navbar.classList.remove('sidebar-collapsed');
            }
        }
    }
    
    checkSidebarState();
    
    function toggleSidebar(e) {
        console.log('Toggle sidebar function called');
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        
        sidebar.classList.toggle('collapsed');
        contentWrapper.classList.toggle('expanded');
        navbar.classList.toggle('sidebar-collapsed');
        
        sidebar.classList.toggle('show');
        sidebarOverlay.classList.toggle('show');
        document.body.classList.toggle('sidebar-open');
        
        const toggleIcon = sidebarToggle.querySelector('i');
        if (toggleIcon) {
            if (sidebar.classList.contains('collapsed')) {
                toggleIcon.classList.remove('fa-times');
                toggleIcon.classList.add('fa-bars');
            } else {
                toggleIcon.classList.remove('fa-bars');
                toggleIcon.classList.add('fa-times');
            }
        }
        
        const isSidebarOpen = !sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarOpen', isSidebarOpen);
        
        console.log('Sidebar toggle clicked, sidebar show:', sidebar.classList.contains('show')); 
    }
    
    if (sidebarToggle) {
        console.log('Adding event listeners to sidebar toggle button');
        sidebarToggle.addEventListener('click', toggleSidebar);
        
        sidebarToggle.addEventListener('touchstart', function(e) {
            console.log('Touchstart on sidebar toggle');
            e.preventDefault();
            toggleSidebar();
        }, { passive: false });
    } else {
        console.error('Sidebar toggle button not found!');
    }
    
    if (sidebarCloseBtn) {
        sidebarCloseBtn.addEventListener('click', function(e) {
            e.preventDefault();
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            navbar.classList.add('sidebar-collapsed');
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
            
            localStorage.setItem('sidebarOpen', false);
        });
        
        sidebarCloseBtn.addEventListener('touchstart', function(e) {
            e.preventDefault();
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            navbar.classList.add('sidebar-collapsed');
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
            
            localStorage.setItem('sidebarOpen', false);
        }, { passive: false });
    }
    
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            navbar.classList.add('sidebar-collapsed');
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
            
            localStorage.setItem('sidebarOpen', false);
        });
        
        sidebarOverlay.addEventListener('touchstart', function(e) {
            e.preventDefault();
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            navbar.classList.add('sidebar-collapsed');
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
            
            localStorage.setItem('sidebarOpen', false);
        }, { passive: false });
    }
    
    document.addEventListener('click', function(event) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggle = sidebarToggle && sidebarToggle.contains(event.target);
        const isClickOnOverlay = sidebarOverlay && sidebarOverlay.contains(event.target);
        
        if (window.innerWidth < 768 && !isClickInsideSidebar && !isClickOnToggle && !isClickOnOverlay && sidebar.classList.contains('show')) {
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            navbar.classList.add('sidebar-collapsed');
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
            
            localStorage.setItem('sidebarOpen', false);
        }
    });
    
    
    function initSidebar() {
        if (window.innerWidth >= 768) {
            const sidebarOpen = localStorage.getItem('sidebarOpen');
            
            if (sidebarOpen !== null && sidebarOpen === 'false') {
                sidebar.classList.add('collapsed');
                contentWrapper.classList.add('expanded');
                navbar.classList.add('sidebar-collapsed');
            } 
            else if (sidebarOpen !== null && sidebarOpen === 'true') {
                sidebar.classList.remove('collapsed');
                contentWrapper.classList.remove('expanded');
                navbar.classList.remove('sidebar-collapsed');
            }
        }
    }
    
    initSidebar();
    
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.nextElementSibling;
            
            document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
                if (menu !== dropdown) {
                    menu.classList.remove('show');
                }
            });
            
            dropdown.classList.toggle('show');
        });
    });
    
    document.addEventListener('click', function(event) {
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        
        dropdowns.forEach(function(dropdown) {
            const toggle = dropdown.previousElementSibling;
            
            if (!dropdown.contains(event.target) && !toggle.contains(event.target)) {
                dropdown.classList.remove('show');
            }
        });
    });
    
    const tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.classList.add('table-responsive');
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
    
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    
    sidebarLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.classList.remove('sidebar-open');
            
            initSidebar();
        } else {
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            navbar.classList.add('sidebar-collapsed');
        }
    });
    
    if (window.innerWidth <= 768) {
        console.log('Mobile view detected, sidebar toggle should be visible');
        if (sidebarToggle) {
            console.log('Sidebar toggle element found:', sidebarToggle);
        } else {
            console.log('Sidebar toggle element NOT found!');
        }
    }

    
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
                document.body.classList.remove('sidebar-open');
            }
        }
    });

    
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768) {
            const isClickInside = sidebar.contains(event.target) || 
                                sidebarToggle.contains(event.target);
            
            if (!isClickInside && document.body.classList.contains('sidebar-open')) {
                toggleSidebar();
            }
        }
    });

    window.addEventListener('load', function() {
        const sidebarOpen = localStorage.getItem('sidebarOpen') === 'true';
        if (!sidebarOpen) {
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
        }
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            contentWrapper.classList.add('expanded');
            document.body.classList.remove('sidebar-open');
        } else {
            const sidebarOpen = localStorage.getItem('sidebarOpen') === 'true';
            if (sidebarOpen) {
                sidebar.classList.remove('collapsed');
                contentWrapper.classList.remove('expanded');
            }
        }
    });
}); 