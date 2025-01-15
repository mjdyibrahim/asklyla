<template>
    <header class="header-container">
      <div class="logo-container">
        <img src="/Lyla-Logo-Modern.png" alt="Lyla Logo">
      </div>
      <nav class="nav-menu">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/destinations">Destinations</a></li>
          <li><a href="/stays">Stays</a></li>
          <li><a href="/experiences">Experiences</a></li>
          <li><a href="/news">Our News</a></li>
        </ul>
      </nav>
    </header>
  </template>
  
  <script setup>
  // No specific script needed for now
  </script>
  
  <style scoped>
  .header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: #00BBD6; /* Match the background color */
    color: white;
  }
  
  .nav-menu ul {
    list-style: none;
    display: flex;
    gap: 20px; /* Space between menu items */
  }
  
  .nav-menu a {
    color: white;
    text-decoration: none;
    font-weight: bold;
  }
  
  .nav-menu a:hover {
    text-decoration: underline; /* Underline on hover */
  }
  </style>