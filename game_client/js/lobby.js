function createRoom() {
  let container = document.getElementById("button_container");
  container.classList.add("hidden_container");

  let createContainer = document.getElementById("create_room_container");
  createContainer.classList.add("show_create_room_container");
}

function showRooms() {
  let container = document.getElementById("button_container");
  container.classList.add("hidden_container");

  let joinContainer = document.getElementById("room_list_container");
  joinContainer.classList.add("show_room_list_container");
}

function backToMenu() {
  let container = document.getElementById("button_container");
  container.classList.remove("hidden_container");
}

function getRoomID() {
  let lobby_name = document.getElementById("lobby_id").value;
  if (!lobby_name.trim()) {
    alert("Please enter a room name.");
    return;
  }
  const playerName = prompt("Enter your name:");
  if (playerName) {
    window.location.href = `/create?lobby_id=${lobby_name}&player_name=${encodeURIComponent(playerName)}`;
  }
}

function setupRoomListObserver() {
  const roomListContainer = document.getElementById("room_list_container");

  // Create observer to watch for class changes
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === "class") {
        // Check if show_room_list_container class was added
        if (roomListContainer.classList.contains("show_room_list_container")) {
          console.log("Room list is now visible!");
          // Do whatever you need here - fetch room list, etc.
          loadAvailableRooms();
        }
      }
    });
  });

  // Start observing
  observer.observe(roomListContainer, {
    attributes: true,
    attributeFilter: ["class"],
  });
}

function loadAvailableRooms() {
  let room_list = document.getElementById("room_list");

  // Fetch available rooms from server
  fetch("/get_rooms")
    .then((response) => response.json())
    .then((data) => {
      // Populate the room list
      console.log("Loading rooms:", data["rooms"]);

      room_list.innerHTML = "";

      let thead = document.createElement("thead");
      let headerRow = document.createElement("tr");
      headerRow.innerHTML = `
                <th>Lobby Name</th>
                <th># of Players</th>
                <th>Join?</th>
            `;
      thead.appendChild(headerRow);
      room_list.appendChild(thead);

      let tbody = document.createElement("tbody");

      data["rooms"].forEach((room) => {
        let row = document.createElement("tr");
        row.innerHTML = `
                    <td>${room["lobby_id"]}</td>
                    <td>${room["num_players"]}/2</td>
                    <td>
                        <button onclick="joinRoom('${room["lobby_id"]}', ${room["num_players"]})" class="btn">
                            Join
                        </button>
                    </td>
                `;
        tbody.appendChild(row);
      });

      room_list.appendChild(tbody);
    });
}

function joinRoom(id, players) {
  if (players != 2) {
    const playerName = prompt("Enter your name:");
    if (playerName) {
      window.location.href = `/join_game?lobby_id=${id}&player_name=${encodeURIComponent(playerName)}`;
    }
  } else {
    alert("Unable to join, room is already full");
  }
}

document.addEventListener("DOMContentLoaded", (event) => {
  console.log("DOM fully loaded and parsed");
  setupRoomListObserver();
});
