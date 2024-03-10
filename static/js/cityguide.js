// Check if the city is set to Cairo
if (city === "Cairo") {
    // Load and display the featured accommodations and experiences
    fetch("cairo.json")
        .then(response => response.json())
        .then(data => {
            // Extract the featured accommodations and experiences from the data
            const featuredAccommodations = data.featuredAccommodations;
            const featuredExperiences = data.featuredExperiences;

            // Update the DOM to display the featured accommodations and experiences
            const featuredAccommodationsContainer = document.getElementById("featuredAccommodations");
            const featuredExperiencesContainer = document.getElementById("featuredExperiences");

            // Populate the containers with the content from the JSON data
            // You can use loops or other methods to create and append HTML elements

            // For example:
            featuredAccommodations.forEach(item => {
                // Create and append HTML elements for each featured accommodation
                const accommodationElement = document.createElement("div");
                // Set inner HTML or text content based on the item data
                accommodationElement.innerHTML = `<h2>${item.title}</h2><p>${item.description}</p>`;
                featuredAccommodationsContainer.appendChild(accommodationElement);
            });

            featuredExperiences.forEach(item => {
                // Create and append HTML elements for each featured experience
                const experienceElement = document.createElement("div");
                // Set inner HTML or text content based on the item data
                experienceElement.innerHTML = `<h2>${item.title}</h2><p>${item.description}</p>`;
                featuredExperiencesContainer.appendChild(experienceElement);
            });
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

// The rest of your code
