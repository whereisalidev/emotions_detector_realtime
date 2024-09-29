function smoothUpdateSlider(slider, targetValue) {
    let currentValue = parseInt(slider.value);
    const increment = (targetValue - currentValue) / 10; 
    const updateInterval = setInterval(() => {
        currentValue += increment;

        if (Math.abs(currentValue - targetValue) < 1) {
            currentValue = targetValue;
            clearInterval(updateInterval);
        }

        slider.value = currentValue;
        slider.dispatchEvent(new Event('input'));
    }, 50); 
}

function updateSliders(emotions) {
    smoothUpdateSlider(document.getElementById('happy-slider'), emotions.happy);
    smoothUpdateSlider(document.getElementById('sad-slider'), emotions.sad);
    smoothUpdateSlider(document.getElementById('neutral-slider'), emotions.neutral);
    smoothUpdateSlider(document.getElementById('angry-slider'), emotions.angry);
    smoothUpdateSlider(document.getElementById('surprise-slider'), emotions.surprise);
    smoothUpdateSlider(document.getElementById('fear-slider'), emotions.fear);

    document.getElementById('happy-percentage').innerText = parseInt(emotions.happy) + '%';
    document.getElementById('sad-percentage').innerText = parseInt(emotions.sad) + '%';
    document.getElementById('neutral-percentage').innerText = parseInt(emotions.neutral) + '%';
    document.getElementById('angry-percentage').innerText = parseInt(emotions.angry) + '%';
    document.getElementById('surprise-percentage').innerText = parseInt(emotions.surprise) + '%';
    document.getElementById('fear-percentage').innerText = parseInt(emotions.fear) + '%';
}

setInterval(() => {
    fetch('/get-emotions/')
        .then(response => response.json())
        .then(data => {
            updateSliders(data);
        })
        .catch(error => console.error('Error fetching emotions:', error));
}, 1000);

// Function to update slider background
function updateSliderBackground(slider) {
    const value = (slider.value - slider.min) / (slider.max - slider.min) * 100;
    slider.style.setProperty('--value', `${value}%`);
}

// Update the background on input
document.querySelectorAll('input[type="range"]').forEach(slider => {
    updateSliderBackground(slider); // Set initial background
    slider.addEventListener('input', () => updateSliderBackground(slider)); // Update on input
});