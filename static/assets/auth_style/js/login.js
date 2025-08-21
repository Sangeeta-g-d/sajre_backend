import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

// Initialize Lottie animation
new DotLottie({
    autoplay: true,
    loop: true,
    canvas: document.getElementById("lottie-canvas"),
    src: "https://lottie.host/9c327513-b85c-4f5f-9224-85c323c9f314/g0y7piHqLL.lottie",
});

// Handle floating labels
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