<script setup>
import { ref } from 'vue'

const city = ref(null)
const searchQuery = ref('')
const errorMessage = ref('')

async function searchCity() {
  try {
    const response = await fetch(`/api/cityguide?city=${searchQuery.value}`, {
      headers: {
        'x-api-key': 'your_api_key_here'
      }
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    city.value = data
    errorMessage.value = ''
    
    if (city.value && city.value.name === 'Cairo') {
      loadFeaturedContent()
    }
  } catch (error) {
    console.error('Error fetching city data:', error)
    errorMessage.value = 'Error fetching city data. Please try again.'
  }
}

async function loadFeaturedContent() {
  try {
    const response = await fetch('/api/cairo.json', {
      headers: {
        'x-api-key': 'your_api_key_here'
      }
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    updateFeaturedContent(data)
  } catch (error) {
    console.error('Error fetching featured content:', error)
    errorMessage.value = 'Error fetching featured content. Please try again.'
  }
}

function updateFeaturedContent(data) {
  const featuredAccommodationsContainer = document.getElementById('featuredAccommodations')
  const featuredExperiencesContainer = document.getElementById('featuredExperiences')

  if (featuredAccommodationsContainer && featuredExperiencesContainer) {
    featuredAccommodationsContainer.innerHTML = ''
    featuredExperiencesContainer.innerHTML = ''

    data.featuredAccommodations.forEach(item => {
      const accommodationElement = document.createElement('div')
      accommodationElement.innerHTML = `<h2>${item.title}</h2><p>${item.description}</p>`
      featuredAccommodationsContainer.appendChild(accommodationElement)
    })

    data.featuredExperiences.forEach(item => {
      const experienceElement = document.createElement('div')
      experienceElement.innerHTML = `<h2>${item.title}</h2><p>${item.description}</p>`
      featuredExperiencesContainer.appendChild(experienceElement)
    })
  }
}
</script>

<template>
  <div class="container">
    <div v-if="city" class="city-guide-container">
      <div class="city-guide-title">
        <h1>City Guide for {{ city.name }}</h1>
      </div>
      <div id="featuredAccommodations"></div>
      <div id="featuredExperiences"></div>
      <div class="city-guide-data">
        <p>Country: {{ city.country }}</p>
        <p>Population: {{ city.population }}</p>
        <!-- ... other city data ... -->
      </div>
    </div>
    <div v-else class="search-container">
      <h1>Search City Guide</h1>
      <form @submit.prevent="searchCity">
        <label for="city">Enter City Name: </label>
        <input v-model="searchQuery" type="text" id="city" required>
        <button type="submit">Search</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  background-color: #f5f5f5;
  padding: 20px;
}

.city-guide-container, .search-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  text-align: center;
}

.city-guide-title h1 {
  color: #00bbd6;
  margin-bottom: 20px;
}

.city-guide-data p {
  margin: 10px 0;
}

#featuredAccommodations, #featuredExperiences {
  margin-top: 20px;
}

.search-container h1 {
  color: #00bbd6;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  margin-bottom: 10px;
  font-weight: bold;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 20px;
  width: 100%;
  max-width: 300px;
}

button {
  background-color: #00bbd6;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #009bb5;
}
</style>