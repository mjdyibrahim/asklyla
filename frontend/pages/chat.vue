<script setup>
import { ref } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { sendMessage } from '~/api/chat'

const { isAuthenticated } = useAuth()

const message = ref('')
const chatMessages = ref([])

const handleSendMessage = async () => {
  if (message.value.trim()) {
    try {
      const response = await sendMessage(message.value)
      chatMessages.value.push({ user: message.value, bot: response.message })
      message.value = ''
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }
}
</script>

<template>
  <div class="chat-container">
    <section class="column-left">
      <div class="upper-nav">          
        <nav>
          <!-- Replace with NuxtLink components -->
          <NuxtLink v-if="isAuthenticated" to="/dashboard">Dashboard</NuxtLink>
          <NuxtLink v-if="isAuthenticated" to="/logout">Logout</NuxtLink>
          <NuxtLink v-else to="/login">Login</NuxtLink>
          <NuxtLink v-else to="/signup">Sign Up</NuxtLink>
        </nav>
      </div>
      
      <div class="chat-header">
        <h1>Lyla is your personal travel companion</h1>
        <p>Lyla helps you enjoy a seamless travel experience through:</p>
        <ul>
          <li>Create itinerary with planned activities and reservations</li>
          <li>Travel packing checklist with recommended items</li>
          <li>24/7 Instant support throughout your trip</li>                
          <li>Travel journal with entries and photos from the trip</li>               
        </ul>
      </div>
      <nav class="nav_list">
        <div v-if="!isAuthenticated">
          <NuxtLink to="/signup"><button id="signup">Signup</button></NuxtLink>
        </div>
        <div v-if="!isAuthenticated">
          <NuxtLink to="/login"><button id="login">Login</button></NuxtLink>
        </div>
        <div>
          <NuxtLink to="/settings"><button id="settings">Settings</button></NuxtLink>
        </div>
      </nav>
      <div>
        <p>Made with ❤️‍ by Lyla Inc.</p>
      </div>
    </section>
    <section class="column-right">
      <div class="chat-body">
        <div v-for="(msg, index) in chatMessages" :key="index">
          <p>You: {{ msg.user }}</p>
          <p>Lyla: {{ msg.bot }}</p>
        </div>
      </div>
      <div class="chat-footer">
        <form @submit.prevent="handleSendMessage">
          <input v-model="message" type="text" placeholder="Type your message...">
          <button type="submit">Send</button>
        </form>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* You can keep your existing CSS here or in a separate file */
</style>