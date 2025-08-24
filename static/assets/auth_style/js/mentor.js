import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lottie animation
    new DotLottie({
        autoplay: true,
        loop: true,
        canvas: document.getElementById("lottie-canvas"),
        src: "https://lottie.host/0038cad6-6505-43bf-9cbe-9b319593e3dc/i8RiuBfVRQ.lottie",
    });

    // File size limits
    const MAX_PASSPORT_PHOTO_SIZE = 2 * 1024 * 1024; // 2MB for passport photo
    const MAX_ID_PROOF_SIZE = 5 * 1024 * 1024; // 5MB for ID proof

    // File upload display with size validation
    document.getElementById('passportPhoto').addEventListener('change', function (e) {
        const fileName = e.target.files[0] ? e.target.files[0].name : 'No file uploaded';
        this.closest('.file-upload').querySelector('.file-name').textContent = fileName;
        
        // Validate file size immediately after selection
        validateInput(this);
    });

    document.getElementById('idProof').addEventListener('change', function (e) {
        const fileName = e.target.files[0] ? e.target.files[0].name : 'No file uploaded';
        this.closest('.file-upload').querySelector('.file-name').textContent = fileName;
        
        // Validate file size immediately after selection
        validateInput(this);
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

        // File input validation with size check
        if (input.type === "file") {
            if (input.hasAttribute("required") && input.files.length === 0) {
                showError(input, "Please upload a file");
                return false;
            }
            
            // Check file size for passport photo
            if (input.id === "passportPhoto" && input.files.length > 0) {
                const file = input.files[0];
                if (file.size > MAX_PASSPORT_PHOTO_SIZE) {
                    showError(input, "Passport photo must be less than 2MB");
                    return false;
                }
            }
            
            // Check file size for ID proof
            if (input.id === "idProof" && input.files.length > 0) {
                const file = input.files[0];
                if (file.size > MAX_ID_PROOF_SIZE) {
                    showError(input, "ID proof must be less than 5MB");
                    return false;
                }
            }
        }

        // Pincode check
        if (input.id === "pincode" && input.value.trim() && !/^\d{6}$/.test(input.value.trim())) {
            showError(input, "Enter a valid 6-digit PIN code");
            return false;
        }

        // City, District, and State should not contain numbers
        if (["city", "district", "state"].includes(input.id) && input.value.trim() && /\d/.test(input.value.trim())) {
            showError(input, "Only letters are allowed");
            return false;
        }

        // Total Experience validation
        if (input.id === "totalExperience" && input.value.trim()) {
            let val = parseFloat(input.value.trim());
            if (isNaN(val)) {
                showError(input, "Enter a valid number");
                return false;
            }
            if (val < 0 || val > 999.9) {
                showError(input, "Value must be between 0 and 999.9");
                return false;
            }
            // Round to 1 decimal place
            input.value = val.toFixed(1);
        }

        showError(input, "");
        return true;
    }

    // Real-time validation
    form.querySelectorAll("input, select, textarea").forEach(input => {
        input.addEventListener("blur", () => validateInput(input));
        input.addEventListener("input", () => validateInput(input));
    });

    // Restrict typing for totalExperience field
    const totalExpInput = document.getElementById("totalExperience");
    if (totalExpInput) {
        totalExpInput.addEventListener("input", () => {
            let val = totalExpInput.value;
            // Allow only digits and dot
            val = val.replace(/[^0-9.]/g, "");
            // Limit to one decimal
            if ((val.match(/\./g) || []).length > 1) {
                val = val.substring(0, val.length - 1);
            }
            totalExpInput.value = val;
        });
    }

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