
        import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

        // Initialize Lottie animation
        new DotLottie({
            autoplay: true,
            loop: true,
            canvas: document.getElementById("lottie-canvas"),
            src: "https://lottie.host/2674716f-689a-4059-a659-550cb4c4af96/Jp2HbWRbOe.lottie",
        });

        // Add focus/blur events for better mobile experience
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

function validateForm() {
    let fullName = document.getElementById("fullName").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;

    // Full name validation (only letters & spaces)
    let nameRegex = /^[A-Za-z\s]+$/;
    if (!nameRegex.test(fullName)) {
        alert("Full Name should contain only letters and spaces.");
        return false;
    }

    // Phone validation (10 digits only)
    let phoneRegex = /^[0-9]{10}$/;
    if (!phoneRegex.test(phone)) {
        alert("Phone number must be exactly 10 digits.");
        return false;
    }

    // Password match validation
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false;
    }

    return true; // ✅ Allow form submit
}

function showToast(message, type="success") {
    let bgColor = "#4caf50"; // default green

    if (type === "error") bgColor = "#f44336";   // red
    else if (type === "info") bgColor = "#2196f3";  // blue
    else if (type === "warning") bgColor = "#ff9800"; // orange

    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: bgColor,
        close: true,
        stopOnFocus: true,
    }).showToast();
}

// ✅ make it accessible globally
window.showToast = showToast;
