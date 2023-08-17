const navToggle = document.querySelector(".nav-button");
const navAside = document.querySelector(".nav-aside");

navToggle.addEventListener("click", () => {
    if (navAside.classList.contains("nav-aside-visible")) {
        navAside.classList.remove("nav-aside-visible");
        navToggle.style.backgroundImage = `url('${window.location.origin}/static/images/assets/hamburger.svg')`;
    } else {
        navAside.classList.add("nav-aside-visible");
        navToggle.style.backgroundImage = `url('${window.location.origin}/static/images/assets/cross.svg')`;
    }
});
