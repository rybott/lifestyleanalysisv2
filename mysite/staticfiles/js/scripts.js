document.getElementById('menu-toggle').addEventListener('click', function() {
    const open_menu = document.getElementById('open_menu');
    const close_menu = document.getElementById('close_menu');
    const toggle_open= document.getElementById('menu-toggle');
    const toggle_close= document.getElementById('menu-toggle2');
    const logo= document.getElementById('Logo');
    const sidebar = document.querySelector('.sidebar');
    open_menu.classList.toggle('collapsed');
    close_menu.classList.toggle('collapsed');
    toggle_open.classList.toggle('collapsed');
    toggle_close.classList.toggle('collapsed');
    logo.classList.toggle('collapsed');
    sidebar.classList.toggle('expanded');
});

document.getElementById('menu-toggle2').addEventListener('click', function() {
    const open_menu = document.getElementById('open_menu');
    const close_menu = document.getElementById('close_menu');
    const toggle_open= document.getElementById('menu-toggle');
    const toggle_close= document.getElementById('menu-toggle2');
    const logo= document.getElementById('Logo');
    const sidebar = document.querySelector('.sidebar');
    open_menu.classList.remove('collapsed');
    close_menu.classList.remove('collapsed');
    toggle_open.classList.remove('collapsed');
    toggle_close.classList.remove('collapsed');
    logo.classList.remove('collapsed');
    sidebar.classList.remove('expanded');
});

const menuLinks = document.querySelectorAll('.menu-item');
menuLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const open_menu = document.getElementById('open_menu');
        const close_menu = document.getElementById('close_menu');
        const toggle_open= document.getElementById('menu-toggle');
        const toggle_close= document.getElementById('menu-toggle2');
        const sidebar = document.querySelector('.sidebar');
        open_menu.classList.remove('collapsed');
        close_menu.classList.remove('collapsed');
        toggle_open.classList.remove('collapsed');
        toggle_close.classList.remove('collapsed');
        sidebar.classList.remove('expanded');
    
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
