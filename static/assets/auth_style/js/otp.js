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

window.collectOTP = collectOTP;
