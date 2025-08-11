import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lottie animation
    new DotLottie({
        autoplay: true,
        loop: true,
        canvas: document.getElementById("lottie-canvas"),
        src: "https://lottie.host/0038cad6-6505-43bf-9cbe-9b319593e3dc/i8RiuBfVRQ.lottie",
    });

    // Step navigation
    const nextButton = document.getElementById('nextButton');
    const backButton = document.getElementById('backButton');

    if (nextButton && backButton) {
        nextButton.addEventListener('click', () => {
            document.getElementById('step1').style.display = 'none';
            document.getElementById('step2').style.display = 'block';
        });

        backButton.addEventListener('click', () => {
            document.getElementById('step2').style.display = 'none';
            document.getElementById('step1').style.display = 'block';
        });
    }

    // File upload display
    document.querySelectorAll('.file-input').forEach(input => {
        input.addEventListener('change', function () {
            let fileName = this.files.length > 0 ? this.files[0].name : "No file uploaded";
            this.closest('.file-upload').querySelector('.file-name').textContent = fileName;
        });
    });

    // Initialize floating labels for all inputs
    function initFloatingLabels() {
        document.querySelectorAll('.form-control').forEach(input => {
            // Check if the input has a value on load
            if (input.value && input.nextElementSibling?.classList.contains('form-label')) {
                input.nextElementSibling.classList.add('active');
            }
            
            // For select elements
            if (input.tagName === 'SELECT' && input.value) {
                input.nextElementSibling.classList.add('active');
            }

            input.addEventListener('focus', function () {
                if (this.nextElementSibling?.classList.contains('form-label')) {
                    this.nextElementSibling.classList.add('active');
                }
            });
            
            input.addEventListener('blur', function () {
                if (!this.value && this.nextElementSibling?.classList.contains('form-label')) {
                    this.nextElementSibling.classList.remove('active');
                }
            });
            
            // For select elements - handle change event
            if (input.tagName === 'SELECT') {
                input.addEventListener('change', function() {
                    if (this.value && this.nextElementSibling?.classList.contains('form-label')) {
                        this.nextElementSibling.classList.add('active');
                    } else if (!this.value && this.nextElementSibling?.classList.contains('form-label')) {
                        this.nextElementSibling.classList.remove('active');
                    }
                });
            }
        });
    }

    // Call the initialization function
    initFloatingLabels();
});