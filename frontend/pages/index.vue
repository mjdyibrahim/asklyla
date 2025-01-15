<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Define sampleQuestions
const sampleQuestions = ref([
  "What are the best attractions in Cairo?",
  "How do I get from the airport to my hotel in Jeddah?",
  "What's the weather like in Istanbul?",
  "What are the best restaurants in Riyadh?"
])

const rotatingCity = ref("Cairo")
const cities = ["Cairo", "Jeddah", "Istanbul", "Riyadh", "Moscow", "Dubai", "Abu Dhabi"]
let cityIndex = 0

const router = useRouter()

const typeCity = () => {
  const city = cities[cityIndex]
  const cityLetters = city.split('')
  let i = 0
  rotatingCity.value = ""

  const typingInterval = setInterval(() => {
    rotatingCity.value += cityLetters[i]
    i++
    if (i >= cityLetters.length) {
      clearInterval(typingInterval)
      setTimeout(() => {
        document.querySelector(".flashing-cursor").textContent = "_"
      }, 500) // Show flashing cursor after a delay
    }
  }, 100) // Typing speed (100ms per character)

  cityIndex = (cityIndex + 1) % cities.length
}

const redirectToChat = (question) => {
  router.push({ path: '/chat', query: { question: encodeURIComponent(question) } })
}

const redirectToCommunityPortal = () => {
  window.location.href = "https://community.asklyla.com";
}

onMounted(() => {
  // Start typing the first city immediately
  typeCity()
  // Repeat typing with the next city every 5 seconds
  setInterval(typeCity, 5000)
})
</script>


<template>
  <div class="splash-container">
    <div class="logo-container">
      <img src="/Lyla-Logo-white-500.png" alt="Lyla Logo">
    </div>
    
    <div class="headline">
      <h1>Your AI Companion to ease the burden of</h1>
      <h1>your next trip to <span id="rotatingCity">{{ rotatingCity }}</span><span class="flashing-cursor">_</span></h1>
    </div>

    <div class="questions-container">
      <h2 class="text-center">Frequently Asked Questions</h2>
      <div class="questions-grid">
        <div class="question-box" @click.prevent="redirectToChat('What are the best attractions in Cairo?')">
          <i class="fas fa-map-marker-alt"></i>
          <p>What are the best attractions in Cairo?</p>
        </div>
        <div class="question-box" @click.prevent="redirectToChat('How do I get from the airport to my hotel in Jeddah?')">
          <i class="fas fa-plane-arrival"></i>
          <p>How do I get from the airport to my hotel in Jeddah?</p>
        </div>
        <div class="question-box" @click.prevent="redirectToChat('What\'s the weather like in Istanbul?')">
          <i class="fas fa-sun"></i>
          <p>What's the weather like in Istanbul?</p>
        </div>
        <div class="question-box" @click.prevent="redirectToChat('What are the best restaurants in Riyadh?')">
          <i class="fas fa-utensils"></i>
          <p>What are the best restaurants in Riyadh?</p>
        </div>
      </div>
      
      <!-- Options Container -->
      <div class="options-container">
        <button class="option-button" @click="redirectToChat('Start a Conversation')">Start a Conversation</button>
        <button class="option-button primary" @click="redirectToCommunityPortal">Visit Community Portal</button>
      </div>
    </div>

    <div class="info-container">
      <div class="info-item">
        <i class="far fa-user"></i>
        <h3>Build your traveler profile</h3>
      </div>
      <div class="info-item">
        <i class="fas fa-ticket-alt"></i>
        <h3>Get your full itinerary</h3>
      </div>
      <div class="info-item">
        <i class="fab fa-rocketchat"></i>
        <h3>Enjoy 24/7 support</h3>
      </div>
    </div>

    <footer>
      <p>Copyright &copy; Lyla Inc</p>
    </footer>
  </div>
</template>

<style scoped>
.splash-container {
  font-family: var(--e-global-typography-primary-font-family), Sans-serif;
  font-weight: var(--e-global-typography-primary-font-weight);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Align items to the start */
  min-height: 100vh; /* Ensure full height */
  margin: 0;
  background-color: #00BBD6;
  color: white;
}

.logo-container {
  margin-top: 40px; /* Adjust margin for logo */
}

.headline {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px 0; /* Adjust margin for headline */
  text-align: center;
}

h1 {
  font-size: 48px;
  font-weight: 900;
  line-height: 1.3;
  margin: 0;
}

.flashing-cursor {
  animation: blink-caret 1s step-end infinite;
}

@keyframes blink-caret {
  from, to {
    border-color: transparent;
  }
  50% {
    border-color: black;
  }
}

.questions-container {
  margin: 40px 0;
}

.questions-grid {
  display: flex; /* Use flexbox for horizontal layout */
  justify-content: space-between; /* Space out the boxes evenly */
  max-width: 1000px; /* Adjust max width to fit all boxes */
  margin: 20px auto; /* Center the grid and add margin */
  flex-wrap: nowrap; /* Prevent wrapping to a new line */
}

.question-box {
  background-color: white;
  color: #00BBD6;
  padding: 20px;
  border: 2px solid #00BBD6; /* Border color */
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s; /* Add border color transition */
  flex: 1; /* Allow boxes to grow equally */
  margin: 0 10px; /* Space between boxes */
  min-width: 200px; /* Minimum width for each box */
}

.question-box:hover {
  background-color: #00BBD6;
  color: white;
  border-color: white; /* Keep white border on hover */
}

.question-box i {
  font-size: 36px; /* Increased icon size for better visibility */
  margin-bottom: 10px; /* Space between icon and text */
}

.options-container {
  display: flex;
  justify-content: center; /* Center the buttons */
  margin-top: 40px; /* Space above the options */
}

.option-button {
  background-color: white; /* Button background */
  color: #00BBD6; /* Button text color */
  border: 2px solid #00BBD6; /* Button border color */
  border-radius: 8px; /* Rounded corners */
  padding: 10px 20px; /* Padding for buttons */
  margin: 0 10px; /* Space between buttons */
  cursor: pointer; /* Pointer cursor */
  transition: background-color 0.3s, color 0.3s; /* Transition for hover effect */
}

.option-button:hover {
  background-color: #00BBD6; /* Change background on hover */
  color: white; /* Change text color on hover */
}

.option-button.primary {
  background-color: #00BBD6; /* More pressing option color */
  color: white; /* Text color for primary button */
}

.info-container {
  display: flex;
  justify-content: space-around;
  margin-top: 100px;
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 150px;
  text-align: center;
}

.info-item i {
  font-size: 72px;
  margin-bottom: 10px;
  color: #fff;
}

.info-item h3 {
  font-size: 32px;
  margin: 0;
  color: #fff;
}

footer {
  margin-top: 60px;
  background-color: #00BBD6; /* Match footer background with the rest of the page */
  color: white; /* Ensure footer text is white */
  width: 100%; /* Full width */
  text-align: center; /* Center text */
  padding: 20px 0; /* Add padding for better spacing */
}
</style>