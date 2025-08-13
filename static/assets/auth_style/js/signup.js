import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

// Lottie animation
new DotLottie({
    autoplay: true,
    loop: true,
    canvas: document.getElementById("lottie-canvas"),
    src: "https://lottie.host/2674716f-689a-4059-a659-550cb4c4af96/Jp2HbWRbOe.lottie",
});

// Floating label behavior
document.querySelectorAll('.form-control').forEach(input => {
    input.addEventListener('focus', function () {
        this.parentElement.querySelector('.form-label').classList.add('active');
    });
    input.addEventListener('blur', function () {
        if (!this.value) {
            this.parentElement.querySelector('.form-label').classList.remove('active');
        }
    });
});

// Toastify notification
function showToast(message, type = "error") {
    const colors = {
        error: "#f44336",
        success: "#4caf50",
        info: "#2196f3",
        warning: "#ff9800"
    };

    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "center",
        backgroundColor: colors[type] || colors.error,
        close: true,
        stopOnFocus: true
    }).showToast();
}
window.showToast = showToast;

// Real-time input restrictions
document.getElementById("fullName")?.addEventListener("input", function () {
    this.value = this.value.replace(/[^A-Za-z\s]/g, ""); // only letters & spaces
});

document.getElementById("phone")?.addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, ""); // only numbers
    if (this.value.length > 10) this.value = this.value.slice(0, 10); // max 10 digits
});

// Form validation
function validateForm() {
    const fullName = document.getElementById("fullName")?.value.trim();
    const phone = document.getElementById("phone")?.value.trim();
    const password = document.getElementById("password")?.value;
    const confirmPassword = document.getElementById("confirmPassword")?.value;

    // Full name check
    if (!/^[A-Za-z\s]+$/.test(fullName)) {
        showToast("Full Name should only contain letters and spaces.", "error");
        return false;
    }

    // Phone number check
    if (!/^\d{10}$/.test(phone)) {
        showToast("Phone number must be exactly 10 digits.", "error");
        return false;
    }

    // Password match check
    if (password !== confirmPassword) {
        showToast("Passwords do not match.", "error");
        return false;
    }

    return true; // All good
}

// Attach validation on submit
document.querySelector("form").addEventListener("submit", function (e) {
    if (!validateForm()) e.preventDefault();
});
