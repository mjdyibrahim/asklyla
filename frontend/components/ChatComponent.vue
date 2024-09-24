<template>
  <div>
    <input v-model="message" placeholder="Type your message" />
    <button @click="sendMessage">Send</button>
    <p v-if="response">{{ response }}</p>
  </div>
</template>

<script>
import { sendMessage } from '~/api/chat.js';

export default {
  data() {
    return {
      message: '',
      response: null
    };
  },
  methods: {
    async sendMessage() {
      try {
        const data = await sendMessage(this.message);
        this.response = data.message;
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  }
};
</script>