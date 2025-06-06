document.getElementById("send-button").addEventListener("click", sendMessage);
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

function sendMessage(messageOverride = null) {
  // Se o argumento for um evento, ignora
  if (messageOverride && messageOverride.isTrusted !== undefined) {
    messageOverride = null;
  }
  const userInputElem = document.getElementById("user-input");
  const userInput =
    messageOverride !== null ? messageOverride : userInputElem.value.trim();
  if (userInput === "") return;

  addMessage(userInput, "user");
  userInputElem.value = "";

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Resposta do backend:", data);
      if (data.tipo === "confirmacao_correcao" && data.correcao_sugerida) {
        addCorrectionSuggestion(data.correcao_sugerida);
      } else {
        addMessage(data.resposta ? String(data.resposta) : "", "bot");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      addMessage("Desculpe, ocorreu um erro. Tente novamente.", "bot");
    });
}

function addCorrectionSuggestion(sugestao) {
  const messagesContainer = document.getElementById("chat-messages");
  const suggestionDiv = document.createElement("div");
  suggestionDiv.classList.add("message", "bot-message");

  suggestionDiv.innerHTML = `Você quis dizer "<b>${sugestao}</b>"? 
        <button id="btn-corr-sim">Sim</button>
        <button id="btn-corr-nao">Não</button>`;

  messagesContainer.appendChild(suggestionDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  document.getElementById("btn-corr-sim").onclick = function () {
    suggestionDiv.remove();
    sendMessage(sugestao);
  };
  document.getElementById("btn-corr-nao").onclick = function () {
    suggestionDiv.remove();
  };
}

function addMessage(text, sender) {
  const messagesContainer = document.getElementById("chat-messages");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", `${sender}-message`);

  // Garante que text é string antes de usar replace
  let formattedText = "";
  if (typeof text === "string") {
    formattedText = text.replace(/\n/g, "<br>");
  } else if (typeof text === "object") {
    formattedText = JSON.stringify(text);
  } else {
    formattedText = String(text);
  }

  messageElement.innerHTML = formattedText;

  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
