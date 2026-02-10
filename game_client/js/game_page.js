function closePopup() {
    let popup = document.getElementById("name-popup");
    let nameInput = document.getElementById("name-input");

    if (nameInput.value.trim() === "") {
        alert("Please enter your name.");
        return;
    }
    else {
        popup.classList.remove("open-popup");
    }
}

function openPopup() {
    let popup = document.getElementById("name-popup");
    popup.classList.add("open-popup");
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");
    openPopup();
});