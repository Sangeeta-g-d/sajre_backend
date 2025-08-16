
    // File upload label display
    document.querySelectorAll(".file-input").forEach(input => {
        input.addEventListener("change", function () {
            const fileName = this.files.length > 0 ? this.files[0].name : "No file uploaded";
            this.closest(".file-upload").querySelector(".file-name").textContent = fileName;
            validateInput(this); // Validate when file is selected
        });
    });

    function showError(input, message) {
        const formGroup = input.closest('.form-group') || input.closest('.file-upload');
        let errorDiv = formGroup.querySelector(".error-message");
        
        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.className = "error-message";
            formGroup.appendChild(errorDiv);
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
        // Required check
        if (input.hasAttribute("required") && !input.value.trim() && input.type !== 'file') {
            showError(input, "This field is required");
            return false;
        }

        // File inputs
        if (input.type === "file" && input.hasAttribute("required") && input.files.length === 0) {
            showError(input, "Please upload a file");
            return false;
        }

        // Pincode format
        if (input.id === "pincode" && input.value.trim() && !/^\d{6}$/.test(input.value.trim())) {
            showError(input, "Enter a valid 6-digit PIN code");
            return false;
        }

        // City/District/State not contain numbers
        const alphaOnlyIds = ["city","district","state"];
        if (alphaOnlyIds.includes(input.id) && /\d/.test(input.value.trim())) {
            showError(input, "Only letters are allowed");
            return false;
        }

        // If all validations pass
        showError(input, "");
        return true;
    }

    // Real-time validation on blur
    document.querySelectorAll("input, select, textarea").forEach(input => {
        input.addEventListener("blur", () => validateInput(input));
    });

    // Submit validation
    document.getElementById("mentorRegistrationForm").addEventListener("submit", (e) => {
        let isValid = true;
        
        document.querySelectorAll("input[required], select[required], textarea[required]").forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            // Scroll to the first error
            const firstError = document.querySelector(".error-message.visible");
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });

