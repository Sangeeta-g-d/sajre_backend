import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lottie animation
    new DotLottie({
        autoplay: true,
        loop: true,
        canvas: document.getElementById("lottie-canvas"),
        src: "https://lottie.host/0038cad6-6505-43bf-9cbe-9b319593e3dc/i8RiuBfVRQ.lottie",
    });

    // File upload display
    document.querySelectorAll('.file-input').forEach(input => {
        input.addEventListener('change', function () {
            let fileName = this.files.length > 0 ? this.files[0].name : "No file uploaded";
            this.closest('.file-upload').querySelector('.file-name').textContent = fileName;
        });
    });

    // Floating labels
    function initFloatingLabels() {
        document.querySelectorAll('.form-control').forEach(input => {
            if (input.value && input.nextElementSibling?.classList.contains('form-label')) {
                input.nextElementSibling.classList.add('active');
            }
            if (input.tagName === 'SELECT' && input.value) {
                input.nextElementSibling.classList.add('active');
            }
            input.addEventListener('focus', () => {
                input.nextElementSibling?.classList.add('active');
            });
            input.addEventListener('blur', () => {
                if (!input.value) {
                    input.nextElementSibling?.classList.remove('active');
                }
            });
            if (input.tagName === 'SELECT') {
                input.addEventListener('change', () => {
                    if (input.value) {
                        input.nextElementSibling?.classList.add('active');
                    } else {
                        input.nextElementSibling?.classList.remove('active');
                    }
                });
            }
        });
    }
    initFloatingLabels();

    // Validation setup
    const form = document.getElementById("mentorRegistrationForm");

    // Add error div to all inputs/selects/textareas
    form.querySelectorAll("input, select, textarea").forEach(input => {
        if (!input.parentElement.querySelector(".error-message")) {
            const errorDiv = document.createElement("div");
            errorDiv.classList.add("error-message");
            input.parentElement.appendChild(errorDiv);
        }
    });

    function showError(input, message) {
        let errorDiv = input.parentElement.querySelector(".error-message");
        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.classList.add("error-message");
            input.parentElement.appendChild(errorDiv);
        }
        if (message) {
            errorDiv.textContent = message;
            errorDiv.classList.add("visible");
            input.classList.add("invalid");
        } else {
            errorDiv.textContent = "";
            errorDiv.classList.remove("visible");
            input.classList.remove("invalid");
        }
    }

   function validateInput(input) {
    if (input.hasAttribute("required") && !input.value.trim()) {
        showError(input, "This field is required");
        return false;
    }

    // File input validation
    if (input.type === "file" && input.hasAttribute("required") && input.files.length === 0) {
        showError(input, "Please upload a file");
        return false;
    }

    // Pincode check
    if (input.id === "pincode" && input.value.trim() && !/^\d{6}$/.test(input.value.trim())) {
        showError(input, "Enter a valid 6-digit PIN code");
        return false;
    }

    // City, District, and State should not contain numbers
    if (
        ["city", "district", "state"].includes(input.id) &&
        /\d/.test(input.value.trim())
    ) {
        showError(input, "Only letters are allowed");
        return false;
    }

    showError(input, "");
    return true;
}

    // Real-time validation
    form.querySelectorAll("input, select, textarea").forEach(input => {
        input.addEventListener("blur", () => validateInput(input));
        input.addEventListener("input", () => validateInput(input));
    });

    // On submit
    form.addEventListener("submit", (e) => {
        let valid = true;
        form.querySelectorAll("input, select, textarea").forEach(input => {
            if (!validateInput(input)) {
                valid = false;
            }
        });
        if (!valid) {
            e.preventDefault();
        }
    });
});
