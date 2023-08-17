const alertWrapper = document.querySelector(".alert");
const alertClose = document.querySelector(".alert__close");

if (alertWrapper) {
    alertClose.addEventListener("click", () => (alertWrapper.style.display = "none"));
}

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let messages = document.querySelectorAll(".alert");
        for (let i = 0; i < messages.length; i++) {
            messages[i].style.display = "none";
        }
    }, 5000);
});
