document.addEventListener('DOMContentLoaded', function () {
    const chatbox = document.getElementById('chatbox');
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');

    form.addEventListener('submit', async function (event) {
        // Prevent the default form submission
        event.preventDefault();

        const userMessage = input.value.trim();
        if (!userMessage) {
            return; // Don't process empty input
        }

        // Display the user's message
        displayMessage(userMessage, 'user');

        try {
            // Send user message to the backend
            const response = await fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token
                },
                body: new URLSearchParams({
                    'message': userMessage,
                }),
            });

            const data = await response.json();
            // Display the bot's response
            displayMessage(data.message, 'bot');
        } catch (error) {
            displayMessage('Error: Unable to connect to the server.', 'bot');
        }

        input.value = ''; // Clear the input field
        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the bottom
    });

    function displayMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = message;
        messageDiv.className = `message ${sender}`;
        chatbox.appendChild(messageDiv);
    }

    // Utility function to get CSRF token from cookies
    function getCookie(name) {
        const cookieValue = document.cookie
            .split('; ')
            .find((row) => row.startsWith(name + '='))
            ?.split('=')[1];
        return cookieValue || '';
    }
});
