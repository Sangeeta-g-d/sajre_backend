// Initialize Lottie animation
new DotLottie({
    autoplay: true,
    loop: true,
    canvas: document.getElementById("lottie-canvas"),
    src: "https://lottie.host/c87b4286-78e8-4812-8bea-a5fc104c5b09/jjZcK4GzdO.lottie",
});

const dropdownBtn = document.getElementById('dropdownBtn');
const dropdownMenu = document.getElementById('dropdownMenu');
const continueBtn = document.getElementById('continueBtn');
const selectedOption = document.getElementById('selectedOption');
const roleInput = document.getElementById('roleInput');

// Toggle dropdown
dropdownBtn.addEventListener('click', function (e) {
    e.stopPropagation(); // Prevent the click from bubbling up to document
    dropdownMenu.classList.toggle('show');
    this.classList.toggle('open');
});

// Close dropdown when clicking outside
document.addEventListener('click', function () {
    dropdownBtn.classList.remove('open');
    dropdownMenu.classList.remove('show');
});

// Handle option selection
function selectCategory(category, icon) {
    selectedOption.innerHTML = `<span style="margin-right: 8px;">${icon}</span>${category}`;
    roleInput.value = category;
    dropdownBtn.classList.remove('open');
    dropdownMenu.classList.remove('show');
    continueBtn.disabled = false;
}

// Make the function available globally
window.selectCategory = selectCategory;