const btn = document.getElementById('menu-btn');
const menu = document.getElementById('menu');
const body = document.querySelector('body');

btn.addEventListener('click', () => {
    menu.classList.toggle('open');
    console.log('clicked');
});