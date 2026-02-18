function createPlayer() {
  let popup = document.getElementById("name-popup");
  let nameInput = document.getElementById("name-input");

  // Pre-fill name if it came from the URL (lobby creator/joiner flow)
  const resolvedName = nameInput.value.trim() || PLAYER_NAME;

  if (!resolvedName) {
    alert("Please enter your name.");
    return;
  }

  popup.classList.remove("open-popup");

  fetch("/join_game", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lobby_id: LOBBY_ID, player_name: resolvedName }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const socket = io();
        socket.on("connect", () => {
          socket.emit("join_lobby", {
            lobby_id: LOBBY_ID,
            player_name: resolvedName,
          });
        });
        socket.on("game_start", (data) => {
          document.getElementById("game-area").style.display = "block";
          console.log(data);
          renderHand(data.hand);
          renderTopCard(data.top_card);
        });
      }
    });
}

document.addEventListener("DOMContentLoaded", () => {
  // Auto-fill the name input if we already have it from the URL
  if (PLAYER_NAME) {
    document.getElementById("name-input").value = PLAYER_NAME;
  }
  openPopup();
});

function openPopup() {
  let popup = document.getElementById("name-popup");
  popup.classList.add("open-popup");
}

function renderHand(hand) {
  const suitMap = {
    "♣": "Clubs",
    "♦": "Diamonds",
    "♥": "Hearts",
    "♠": "Spades",
  };

  const handDiv = document.getElementById("player-hand");
  handDiv.innerHTML = "";

  const caption = document.createElement("body");
  caption.textContent = "Player Hand:";
  handDiv.appendChild(caption);

  hand.forEach((card) => {
    const img = document.createElement("img");
    img.src = `/assets/cards/${suitMap[card.suit]}/${card.rank}${card.suit}.jpg`;
    img.alt = `${card.rank}${card.suit}`;
    img.classList.add("card");
    img.style = "width: 80px;";
    handDiv.appendChild(img);
  });
}

function renderTopCard(card) {
  const suitMap = {
    "♣": "Clubs",
    "♦": "Diamonds",
    "♥": "Hearts",
    "♠": "Spades",
  };

  const topCardDiv = document.getElementById("top-card");
  topCardDiv.innerHTML = "";

  const caption = document.createElement("body");
  caption.textContent = "Top Card:";
  topCardDiv.appendChild(caption);

  const img = document.createElement("img");
  img.src = `/assets/cards/${suitMap[card.suit]}/${card.rank}${card.suit}.jpg`;
  img.alt = `${card.rank}${card.suit}`;
  img.style = "width: 80px;";
  img.classList.add("card");
  topCardDiv.appendChild(img);
}
