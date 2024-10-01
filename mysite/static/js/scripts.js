document.getElementById('menu-toggle').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar-wrapper');
    const icons = document.getElementById('Icon');
    const menu = document.getElementById('menu_open');
    const menu_hidden = document.getElementById('menu_collapsed');
    const name1 = document.getElementById('Main_name');
    sidebar.classList.toggle('collapsed');
    icons.classList.toggle('collapsed');
    menu.classList.toggle('collapsed');
    menu_hidden.classList.toggle('collapsed');
    name1.classList.toggle('collapsed');
});

const menuLinks = document.querySelectorAll('.menu-item');
menuLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const sidebar = document.getElementById('sidebar-wrapper');
        const mainContent = document.getElementById('page-content-wrapper');
        const menu = document.getElementById('menu_open');
        const menu_hidden = document.getElementById('menu_collapsed');
        const name1 = document.getElementById('Main_name');
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('collapsed');
        menu.classList.remove('collapsed');
        menu_hidden.classList.remove('collapsed');
        name1.classList.remove('collapsed');
        
        // Here you would add logic to navigate to the correct page
        // For demonstration, just log the clicked menu item
        console.log(`Navigating to: ${link.textContent.trim()}`);
    });
});

function adjustDivWidth() {
    const container = document.getElementById('sidebar-wrapper');
    const resizeLogo = document.getElementById('Logo');
    const resizeName = document.getElementById('Main_name')
    const containerWidth = container.offsetWidth;
    if (containerWidth < 100){
        resizeLogo.style.width = '100%';
        resizeName.style.display = 'none'}
    else{resizeLogo.style.width = '50%'; resizeName.style.display = 'block' }
    }

const container = document.getElementById('sidebar-wrapper');
const observer = new ResizeObserver(adjustDivWidth);
observer.observe(container);
adjustDivWidth();
