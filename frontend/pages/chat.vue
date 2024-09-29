<template>
  <div class="flex h-screen">
    <section class="flex flex-col items-center justify-between w-1/5 text-white bg-teal-500 column-left">
      <div class="upper-nav">
        <!-- Add navigation links -->
        <nav>
          <template v-if="isAuthenticated">
            <a href="/dashboard">Dashboard</a>
            <a href="/logout">Logout</a>
          </template>
        </nav>
      </div>

      <div class="p-4 chat-header">
        <h1 class="text-2xl">Lyla is your personal travel companion</h1>
        <p>Lyla helps you enjoy a seamless travel experience through:</p>
        <ul>
          <li>Create itinerary with planned activities and reservations</li>
          <li>Travel packing checklist with recommended items</li>
          <li>24/7 Instant support throughout your trip</li>
          <li>Travel journal with entries and photos from the trip</li>
        </ul>
      </div>

      <nav class="flex flex-col items-center nav_list">
        <template v-if="!isAuthenticated">
          <div><a href="/signup"><button id="signup" value="Signup" class="btn">Signup</button></a></div>
          <div><a href="/signin"><button id="signin" value="Signin" class="btn">Signin</button></a></div>
        </template>
        <div><a href="/settings"><button id="settings" value="Settings" class="btn">Settings</button></a></div>
      </nav>
      <div>
        <p>Made with ❤️‍ by Lyla Inc.</p>
      </div>
    </section>

    <section class="flex flex-col justify-between w-4/5 bg-white column-right">
      <div class="flex-1 p-4 overflow-y-auto chat-body" ref="chatBody">
        <div v-for="(msg, index) in chatMessages" :key="index" :class="msg.className">
          <div v-if="msg.className === 'user-message'" class="user-message-content">
            <p>{{ msg.text }}</p>
          </div>
          <div v-if="msg.className === 'lyla-message'" class="lyla-message-content">
            <p>{{ msg.text }}</p>
          </div>
        </div>
      </div>
      <div class="flex p-4 bg-gray-200 chat-footer">
        <form @submit.prevent="handleSendMessage" class="flex items-center justify-between w-full p-2 bg-white rounded-full shadow">
          <input v-model="message" type="text" name="message" placeholder="Type your message..." class="flex-1 p-2 border-none rounded-full outline-none">
          <button type="submit" class="btn">Send</button>
        </form>
        <button @click="toggleVoiceInput" class="btn">{{ isVoiceInputEnabled ? 'Stop' : 'Start' }} Voice Input</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useRoute } from 'vue-router'

const { isAuthenticated } = useAuth()
const route = useRoute()

const message = ref('')
const chatMessages = ref([])
const chatBody = ref(null)

const handleSendMessage = async (incomingMessage = null) => {
  const msg = incomingMessage || message.value.trim()
  if (msg) {
    try {
      appendMessage(msg, 'user-message')
      const generatingMessageIndex = appendMessage("Generating response...", 'lyla-message')
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: msg })
      });
      const data = await response.json();
      chatMessages.value.splice(generatingMessageIndex, 1); // Remove the "Generating response..." message
      appendMessage(data.message, 'lyla-message');
      if (data.voice) {
        playAudio(data.voice);
      }
      message.value = ''; // Clear the message input box
    } catch (error) {
      console.error('Failed to send message:', error);
      chatMessages.value.splice(generatingMessageIndex, 1); // Remove the "Generating response..." message
      appendMessage("Sorry, I encountered an error. Please try again.", 'lyla-message');
    }
  }
}

const appendMessage = (text, className) => {
  const newMessage = { text, className }
  chatMessages.value.push(newMessage)
  scrollToBottom()
  return chatMessages.value.length - 1; // Return the index of the new message
}

const scrollToBottom = () => {
  if (chatBody.value) {
    chatBody.value.scrollTop = chatBody.value.scrollHeight
  }
}

const playAudio = (base64Audio) => {
  const audio = new Audio("data:audio/mp3;base64," + base64Audio);
  audio.play();
}

onMounted(() => {
  const incomingQuestion = route.query.question
  if (incomingQuestion) {
    chatMessages.value = []
    appendMessage(decodeURIComponent(incomingQuestion), 'user-message')
    handleSendMessage(decodeURIComponent(incomingQuestion))
  }
})

// Voice input functions
let recognition
const isVoiceInputEnabled = ref(false)

const startDictation = () => {
  if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = "en-US"
    recognition.start()

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript
      message.value = transcript
      handleSendMessage()
      recognition.stop()
    }

    recognition.onerror = () => {
      recognition.stop()
    }
  }
}

const stopDictation = () => {
  if (recognition) {
    recognition.stop()
    recognition = null
  }
}

const toggleVoiceInput = () => {
  isVoiceInputEnabled.value = !isVoiceInputEnabled.value
  if (isVoiceInputEnabled.value) {
    startDictation()
  } else {
    stopDictation()
  }
}

// Auth functions
const signup = async (email, password) => {
  try {
    const response = await fetch('/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })
    const data = await response.json()
    if (data.message) {
      alert(data.message)
    } else {
      alert(data.error)
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

const signin = async (email, password) => {
  try {
    const response = await fetch('/api/signin', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })
    const data = await response.json()
    if (data.message) {
      alert(data.message)
      // Refresh the page or update UI to reflect logged-in state
    } else {
      alert(data.error)
    }
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>

<style scoped>
/* Add your custom styles here */
.btn {
  @apply border-2 border-white py-2 px-4 m-1 transition-colors duration-300 bg-transparent text-white;
}

.btn:hover {
  @apply bg-white text-teal-500;
}

.user-message-content, .lyla-message-content {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
}

.user-message-content {
  background-color: #7ddff0;
  align-self: flex-end;
}

.lyla-message-content {
  background-color: #0099b3;
  align-self: flex-start;
}
</style>