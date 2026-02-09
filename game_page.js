function closePopup() {
    let popup = document.getElementById("name-popup");
    popup.classList.remove("open-popup");
}

function openPopup() {
    let popup = document.getElementById("name-popup");
    popup.classList.add("open-popup");
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");
    openPopup();
});