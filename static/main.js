function toggleTheme() {
    if (localStorage.getItem("theme") == "dark") {
        document.body.setAttribute("data-bs-theme", "light")
        localStorage.setItem("theme", "light")
    } else {
        document.body.setAttribute("data-bs-theme", "dark")
        localStorage.setItem("theme", "dark")
    }
}

function start() {
    if (localStorage.getItem("theme") == "dark") {
        document.body.setAttribute("data-bs-theme", "dark")
    }
}