const chatForm = document.getElementById('chat-form');
const chatBody = document.getElementById('chat-body');

$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const incomingQuestion = urlParams.get('question');

    if (incomingQuestion) {
        // Clear any existing messages in the chat body
        $('#chat-body').empty();
        
        // Display the incoming question in the chat
        appendMessage(decodeURIComponent(incomingQuestion), 'user-message');
        
        // Display a "generating response" message
        const generatingMessage = appendMessage("Generating response...", 'lyla-message');
        
        // Send the incoming question to the chat
        sendMessage(incomingQuestion, generatingMessage);
    } else {
        // If there's no incoming question, display the initial Lyla message
        appendMessage("Hi, I'm Lyla, your personal travel companion. How can I assist you with your travel plans today?", 'lyla-message');
    }

    $('#chat-form').on('submit', function(e) {
        e.preventDefault();
        var userMessage = $('input[name="message"]').val();
        appendMessage(userMessage, 'user-message');
        $('input[name="message"]').val('');

        $.ajax({
            url: '/chat',  // Update this line to use the new /chat endpoint
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: userMessage }),
            success: function(response) {
                appendMessage(response.message, 'lyla-message');
                playAudio(response.voice);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
                appendMessage("Sorry, I encountered an error. Please try again.", 'lyla-message');
            }
        });
    });

    function appendMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        
        if (className === 'user-message') {
            messageElement.innerHTML = `
                <div class="user-message-content">
                    <p>${message}</p>
                </div>
                <div class="user-message-icon">
                    <img src="/static/user.png" alt="user icon">
                </div>
            `;
        } else if (className === 'lyla-message') {
            messageElement.innerHTML = `
                <div class="lyla-message-icon">
                    <img src="/static/lyla.png" alt="Lyla icon">
                </div> 
                <div class="lyla-message-content">
                    <p>${message}</p>
                </div>
            `;
        }
        
        chatBody.appendChild(messageElement);
        chatBody.scrollTop = chatBody.scrollHeight;
        return messageElement;
    }

    function playAudio(base64Audio) {
        let audio = new Audio("data:audio/mp3;base64," + base64Audio);
        audio.play();
    }

    function playVoiceOutput(base64Audio) {
        const audio = new Audio("data:audio/mp3;base64," + base64Audio);
        audio.play();
    }

    function sendMessage(message, generatingMessage = null) {
        $.ajax({
            url: '/chat',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function(response) {
                if (generatingMessage) {
                    // Remove the "generating response" message
                    generatingMessage.remove();
                }
                appendMessage(response.message, 'lyla-message');
                playAudio(response.voice);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
                if (generatingMessage) {
                    // Update the "generating response" message with an error
                    generatingMessage.querySelector('p').textContent = "Sorry, I encountered an error. Please try again.";
                } else {
                    appendMessage("Sorry, I encountered an error. Please try again.", 'lyla-message');
                }
            }
        });
    }
});

function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(e) {
            const transcript = e.results[0][0].transcript;
            addMessage('user', transcript);
            sendMessage(transcript);
            recognition.stop();
        };

        recognition.onerror = function(e) {
            recognition.stop();
        }
    }
}

function stopDictation() {
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
}

var isVoiceInputEnabled = false;
function toggleVoiceInput() {
    isVoiceInputEnabled = !isVoiceInputEnabled;
    if (isVoiceInputEnabled) {
        startDictation();
    } else {
        stopDictation();
    }
}

// Add these functions to your existing script.js

function signup() {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            // Refresh the page or update UI to reflect logged-in state
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}