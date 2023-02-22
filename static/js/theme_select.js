const themeForm = document.getElementById('theme-form')
const updateTheme = () => {
    const theme = themeForm.querySelector('input[name="theme"]:checked').value
    const link = document.querySelector('#theme-select')

    if (theme === 'auto') {
        link.setAttribute('href', 'css/light.css')
    } else if (theme === 'light') {
        link.setAttribute('href', 'css/light.css')
    
    } else if (theme === 'dark') {
        link.setAttribute('href', 'css/dark.css')
    }
}

themeForm.addEventListener('change', updateTheme)

export {}
