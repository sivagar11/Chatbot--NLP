function sendMessage() {
    var userInput = document.getElementById("user-input");
    var chatLog = document.getElementById("chat-log");

    // Create user chat bubble element
    var userBubble = document.createElement("div");
    userBubble.classList.add("chat-bubble");

    // Create message element inside the user bubble
    var userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.innerHTML = "<strong>You:</strong> " + userInput.value;

    // Append message element to the user bubble
    userBubble.appendChild(userMessage);

    // Append user bubble to the chat log
    chatLog.appendChild(userBubble);

    // Send user message to the server
    $.post("/get_response", { message: userInput.value }, function(data) {
        // Create bot chat bubble element
        var botBubble = document.createElement("div");
        botBubble.classList.add("chat-bubble");

        // Create message element inside the bot bubble
        var botMessage = document.createElement("div");
        botMessage.classList.add("message");
        botMessage.innerHTML = "<strong>Bot:</strong> " + data;

        // Append message element to the bot bubble
        botBubble.appendChild(botMessage);

        // Append bot bubble to the chat log
        chatLog.appendChild(botBubble);

        // Scroll to the bottom of the chat log
        chatLog.scrollTop = chatLog.scrollHeight;
    });

    // Clear the input field
    userInput.value = "";
}

// Submit form on Enter key press
$("#user-input").on("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        sendMessage();
    }
});

// Handle send button click
$("#send-button").click(function(event) {
    event.preventDefault();
    sendMessage();
});
