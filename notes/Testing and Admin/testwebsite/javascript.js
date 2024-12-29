document.getElementById('menu-toggle').addEventListener('click', function() {
    const open_menu = document.getElementById('open_menu');
    const close_menu = document.getElementById('close_menu');
    const toggle_open= document.getElementById('menu-toggle');
    const toggle_close= document.getElementById('menu-toggle2');
    const sidebar = document.querySelector('.sidebar');
    open_menu.classList.toggle('collapsed');
    close_menu.classList.toggle('collapsed');
    toggle_open.classList.toggle('collapsed');
    toggle_close.classList.toggle('collapsed');
    sidebar.classList.toggle('expanded');
});

document.getElementById('menu-toggle2').addEventListener('click', function() {
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

