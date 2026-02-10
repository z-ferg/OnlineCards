function createRoom() {
    let container = document.getElementById("button_container");
    container.classList.add("hidden_container");

    let createContainer = document.getElementById("create_room_container");
    createContainer.classList.add("show_create_room_container");
}

function joinRoom() {
    let container = document.getElementById("button_container");
    container.classList.add("hidden_container");

    let joinContainer = document.getElementById("room_list_container");
    joinContainer.classList.add("show_room_list_container");
}

function backToMenu() {
    let container = document.getElementById("button_container");
    container.classList.remove("hidden_container");
}