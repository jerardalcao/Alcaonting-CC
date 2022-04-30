const sidebarToggle = document.querySelector(".sidebar-button")
const sidebar = document.querySelector(".sidebar")

sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("hide");
    sidebarToggle.classList.toggle("icon");
})

const dropdownToggle = document.querySelector(".dropdown")
const dropdown = document.querySelector(".dropdown-list")

dropdownToggle.addEventListener("click", () => {
    dropdown.classList.toggle("hide");
})