import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

// Initialize Lottie animation
new DotLottie({
    autoplay: true,
    loop: true,
    canvas: document.getElementById("lottie-canvas"),
    src: "https://lottie.host/5db068f5-a840-4848-9fea-b997dfca7b07/cPpdwG703i.lottie",
});

// OTP input handling
const otpInputs = document.querySelectorAll('.otp-input');
const hiddenOtpField = document.getElementById("otp_code");

otpInputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
        if (e.target.value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && e.target.value.length === 0 && index > 0) {
            otpInputs[index - 1].focus();
        }
    });
});

// ✅ Collect OTP before form submit
function collectOTP() {
    let otp = "";
    otpInputs.forEach(input => otp += input.value);
    hiddenOtpField.value = otp;  
    console.log("Collected OTP:", otp); // 👀 Debug log
    return true; // allow form submit
}

// ===========  Countdown Timer  ===========
let timeLeft = window.otpData.remainingSeconds;
const countdownEl = document.getElementById("countdown");
const resendBtn   = document.getElementById("resendBtn");

// Make timer global
let timer;

function startCountdown() {
    // Clear any existing timer first
    if (timer) {
        clearInterval(timer);
    }

    timer = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(timer);
            countdownEl.innerText = "OTP expired";
            resendBtn.style.display = "inline-block";
            return;
        }
        const mins = Math.floor(timeLeft / 60);
        const secs = timeLeft % 60;
        countdownEl.innerText =
            `OTP valid for ${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
        timeLeft--;
    }, 1000);
}

// ===========  Resend OTP via AJAX  ===========
function resendOTP(userId) {
    fetch(`/auth/resend-otp/${userId}/`, {
        method: "POST",
        headers: {
            'X-CSRFToken': window.otpData.csrfToken,
            'Accept': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status) {
            showToast(data.message, "success");

            // Reset timer
            timeLeft = data.remaining_seconds;
            resendBtn.style.display = "none";
            startCountdown();
        } else {
            showToast(data.message, "error");
        }
    })
    .catch(error => {
        showToast("An error occurred while resending OTP", "error");
        console.error("Error:", error);
    });
}

function showToast(message, type = "success") {


   Toastify({
    text: message,
    duration: 3000,
    close: true,
    gravity: "top",
    position: "right",
    stopOnFocus: true,
    style: {
        background: type === "success"
            ? "linear-gradient(to right, #00b09b, #96c93d)"
            : "linear-gradient(to right, #ff5f6d, #ffc371)"
    }
}).showToast();
}

// Run timer initially
if (timeLeft > 0) {
    startCountdown();
} else if (countdownEl) {
    countdownEl.innerText = "OTP expired";
    if (resendBtn) resendBtn.style.display = "inline-block";
}

// Show error toast if exists
if (window.otpData.error) {
    showToast(window.otpData.error, "error");
}

// Make functions available globally
window.collectOTP = collectOTP;
window.resendOTP = resendOTP;
window.showToast = showToast;