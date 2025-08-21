import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

// Lottie animation
new DotLottie({
    autoplay: true,
    loop: true,
    canvas: document.getElementById("lottie-canvas"),
    src: "https://lottie.host/2674716f-689a-4059-a659-550cb4c4af96/Jp2HbWRbOe.lottie",
});

// Toastify notification function
function showToast(message, type = "error") {
    const colors = {
        error: "linear-gradient(to right, #ff5f6d, #ffc371)",
        success: "linear-gradient(to right, #00b09b, #96c93d)",
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
window.showToast = showToast; // Make it globally accessible

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

// Real-time input restrictions
document.getElementById("fullName")?.addEventListener("input", function () {
    this.value = this.value.replace(/[^A-Za-z\s]/g, ""); // only letters & spaces
});

document.getElementById("phone")?.addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, ""); // only numbers
    if (this.value.length > 10) this.value = this.value.slice(0, 10); // max 10 digits
});

// Function to validate password requirements
function validatePassword(password) {
    const errors = [];
    if (password.length < 8) errors.push("8 chars");
    if (!/[0-9]/.test(password)) errors.push("one number");
    if (!/[A-Z]/.test(password)) errors.push("one uppercase");
    if (!/[a-z]/.test(password)) errors.push("one lowercase");
    return errors;
}

// Real-time password validation
document.getElementById("password")?.addEventListener("input", function () {
    const password = this.value;
    const errorElement = document.getElementById("password-error");
    const errors = validatePassword(password);

    if (password.length === 0) {
        errorElement.style.display = "none";
        errorElement.textContent = "";
    } else if (errors.length > 0) {
        errorElement.textContent =  "Atleast : " + errors.join(", ");
        errorElement.style.display = "block";
    } else {
        errorElement.style.display = "none";
        errorElement.textContent = "";
    }
});

// Confirm password validation
document.getElementById("confirmPassword")?.addEventListener("input", function () {
    const password = document.getElementById("password")?.value;
    const confirmPassword = this.value;
    const errorElement = document.getElementById("confirm-password-error");
    
    if (confirmPassword.length === 0) {
        errorElement.style.display = "none";
        errorElement.textContent = "";
    } else if (password !== confirmPassword) {
        errorElement.textContent = "Passwords do not match";
        errorElement.style.display = "block";
    } else {
        errorElement.style.display = "none";
        errorElement.textContent = "";
    }
});

// Enhanced form validation
function validateForm() {
    const fullName = document.getElementById("fullName")?.value.trim();
    const email = document.getElementById("email")?.value.trim();
    const phone = document.getElementById("phone")?.value.trim();
    const password = document.getElementById("password")?.value;
    const confirmPassword = document.getElementById("confirmPassword")?.value;

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Full name check
    if (!/^[A-Za-z\s\-'.]+$/.test(fullName)) {
        showToast("Name should only contain letters, spaces, hyphens, apostrophes, and periods.", "error");
        return false;
    }
    
    // Email check
    if (!emailRegex.test(email)) {
        showToast("Please enter a valid email address.", "error");
        return false;
    }

    // Phone number check
    if (!/^\d{10}$/.test(phone)) {
        showToast("Phone number must be exactly 10 digits.", "error");
        return false;
    }

    // Password requirements check
    const passwordErrors = validatePassword(password);
    if (passwordErrors.length > 0) {
        showToast(`Password must contain: ${passwordErrors.join(", ")}.`, "error");
        return false;
    }

    // Password match check
    if (password !== confirmPassword) {
        showToast("Passwords do not match.", "error");
        return false;
    }

    return true; // All validations passed
}

// Form submit handler - FIXED VERSION
document.getElementById("signupForm").addEventListener("submit", function (e) {
    // Prevent default submission to run custom validation first
    e.preventDefault();

    if (validateForm()) {
        // Disable submit button to prevent double submissions
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        submitBtn.disabled = true;
        submitBtn.textContent = "Creating Account...";
        
        // If all checks pass, submit the form programmatically
        setTimeout(() => {
            this.submit();
        }, 500);
        
        // Re-enable button after 5 seconds in case submission fails
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }, 5000);
    }
});

// Function to toggle password visibility
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    const eyeIcon = btn.querySelector('.password-eye i');
    if (input.type === "password") {
        input.type = "text";
        eyeIcon.classList.remove('bi-eye');
        eyeIcon.classList.add('bi-eye-slash');
    } else {
        input.type = "password";
        eyeIcon.classList.remove('bi-eye-slash');
        eyeIcon.classList.add('bi-eye');
    }
}
window.togglePasswordVisibility = togglePasswordVisibility;