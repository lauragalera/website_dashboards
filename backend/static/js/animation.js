document.addEventListener("DOMContentLoaded", () => {
    const imageList = JSON.parse(document.getElementById("image-data").textContent);
    const leftContainer = document.querySelector('.left-container');
    const rightContainer = document.querySelector('.right-container');
  
    let currentIndex = 0; // Track current index in the array
    const previousPositions = []; // Store the last 4 positions
    const maxTrackedPositions = 4; // Keep track of the last 4 positions
    let isLeft = true; // Track whether to place on the left or right
  
    // Function to get a random position without overlapping
    function getRandomPosition(maxWidth, maxHeight, container) {
        let position;
        let tooClose;
        let attempts = 0;
        const maxAttempts = 50; // Max number of attempts to find a non-overlapping position
  
        do {
            position = {
                x: Math.random() * (container.offsetWidth - maxWidth),
                y: Math.random() * (container.offsetHeight - maxHeight)
            };
  
            // Check if the new position is too close to any of the last 4 positions
            tooClose = previousPositions.some(prev =>
                Math.abs(prev.x - position.x) < 120 && Math.abs(prev.y - position.y) < 500
            );
  
            attempts++;
        } while (tooClose && attempts < maxAttempts); // Retry if too close to any position
  
        return position;
    }
  
    function showNextImage() {
        if (imageList.length === 0) return;
  
        // Get the next image in sequence
        const imgSrc = imageList[currentIndex];
        const img = document.createElement("img");
        img.src = `/static/images/${imgSrc}`;
        img.className = "floating-image";
  
        // Alternate between left and right containers
        const container = isLeft ? leftContainer : rightContainer;
        isLeft = !isLeft; // Toggle between left and right for the next image
  
        let position = getRandomPosition(150, 150, container);
        img.style.left = `${position.x}px`;
        img.style.top = `${position.y}px`;
  
        container.appendChild(img);
  
        // Store the new position in the previousPositions array
        previousPositions.push(position);
        if (previousPositions.length > maxTrackedPositions) {
            previousPositions.shift(); // Keep only the last 4 positions
        }
  
        // Start fade-out effect after 4 seconds
        setTimeout(() => {
            img.style.opacity = "0"; // Begin fade-out animation
        }, 4000);
  
        // Remove the image after 6 seconds (after fade-out animation)
        setTimeout(() => {
            img.remove(); // Remove the image from the DOM
        }, 6000); // The image disappears after the fade-out effect
  
        // Move to the next image, looping back if needed
        currentIndex = (currentIndex + 1) % imageList.length;
    }
  
    // Show the first image immediately, then every 1.5 seconds
    showNextImage();
    setInterval(showNextImage, 1500);
});
