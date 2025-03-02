
const themeToggleBtn = document.getElementById('theme-toggle');
const body = document.body;


const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'dark') {
    body.classList.add('dark-mode');
    themeToggleBtn.textContent = '🌙';
} else {
    body.classList.remove('dark-mode');
    themeToggleBtn.textContent = '🌞';
}


themeToggleBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDarkMode = body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    themeToggleBtn.textContent = isDarkMode ? '🌙' : '🌞';
});
