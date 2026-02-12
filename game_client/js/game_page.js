function createPlayer() {
    let popup = document.getElementById("name-popup");
    let nameInput = document.getElementById("name-input");

    if (nameInput.value.trim() === "") {
        alert("Please enter your name.");
        return;
    }

    popup.classList.remove("open-popup");

    const urlParams = new URLSearchParams(window.location.search)
    const lobby_id = urlParams.get('lobby_id')

    fetch('/join_game', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            lobby_id: lobby_id,
            player_name: nameInput.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Successfully joined game")
        }
    })
}

function openPopup() {
    let popup = document.getElementById("name-popup");
    popup.classList.add("open-popup");
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");
    openPopup();
});