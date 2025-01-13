console.log("background.js loaded");

let backgrounds = window.backgrounds;
console.log("Background images:", backgrounds);

let currentIndex = 0;

function changeBackground() {
    const bg = document.getElementById('background');
    console.log("Changing background to:", backgrounds[currentIndex]);
    bg.style.opacity = 0; // Fade out
    setTimeout(() => {
        bg.style.backgroundImage = `url(${backgrounds[currentIndex]})`;
        bg.style.opacity = 1; // Fade in
        currentIndex = (currentIndex + 1) % backgrounds.length;
    }, 1000); // Wait 1 second before switching
}

setInterval(changeBackground, 5000); // Change background every 5 seconds
changeBackground(); // Set initial background
