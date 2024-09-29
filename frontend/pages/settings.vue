<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded shadow-md">
      <h2 class="text-2xl font-bold text-center">Settings</h2>
      <form @submit.prevent="handleSaveSettings">
        <div class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
            <input v-model="username" type="text" id="username" class="w-full px-3 py-2 border rounded" required>
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input v-model="email" type="email" id="email" class="w-full px-3 py-2 border rounded" required>
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input v-model="password" type="password" id="password" class="w-full px-3 py-2 border rounded" required>
          </div>
          <div>
            <button type="submit" class="w-full btn-primary">Save Settings</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const password = ref('')

const handleSaveSettings = () => {
  // Handle save settings logic
  console.log('Settings saved:', { username: username.value, email: email.value, password: password.value })
}
</script>

<style scoped>
/* Add any additional styles here */
</style>
