import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

// Initialize Lottie animation
new DotLottie({
    autoplay: true,
    loop: true,
    canvas: document.getElementById("lottie-canvas"),
    src: "https://lottie.host/1197e7ab-7b58-48f7-86e9-6706d1dc8756/ly3NSmJS9W.lottie",
});


document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    // Create error containers for all inputs/selects/textareas
    form.querySelectorAll("input, select, textarea").forEach(input => {
        if (!input.parentElement.querySelector(".error-message")) {
            const errorDiv = document.createElement("div");
            errorDiv.classList.add("error-message");
            input.parentElement.appendChild(errorDiv);
        }
    });

    // Validation rules (college fields omitted - optional)
   const validators = {
    // Personal details
    fatherName: value => /^[A-Za-z\s]+$/.test(value) || "Father's name should contain only letters",
    motherName: value => /^[A-Za-z\s]+$/.test(value) || "Mother's name should contain only letters",
    dob: value => {
        if (!value.trim()) return "Date of Birth is required";
        
        const dob = new Date(value);
        const today = new Date();
        let age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();
        
        // Adjust age if birthday hasn't occurred yet this year
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
            age--;
        }
        
        return age >= 9 || "You must be at least 9 years old to register";
    },
    fullAddress: value => value.trim().length >= 5 || "Address should be at least 5 characters",
    streetAddress: value => value.trim().length >= 3 || "Street address should be at least 3 characters",
    city: value => /^[A-Za-z\s]+$/.test(value) || "City should contain only letters",
    district: value => /^[A-Za-z\s]+$/.test(value) || "District should contain only letters",
    state: value => /^[A-Za-z\s]+$/.test(value) || "State should contain only letters",
    pincode: value => /^\d{6}$/.test(value) || "Pincode must be exactly 6 digits",
    dobProof: value => value !== "" || "Please upload a proof of DOB",
    photoUpload: value => value !== "" || "Please upload a photo",

    // School - required
    schoolName: value => value.trim().length >= 2 || "School name is required",
    schoolBoard: value => value.trim() !== "" || "Please select a board",
    schoolLocation: value => value.trim().length >= 2 || "School location is required",

    // College - optional (validate only if filled)
    courseName: value => value.trim() === "" || value.trim().length >= 2 || "Course name must be at least 2 characters",
    university: value => value.trim() === "" || value.trim().length >= 2 || "University is too short",
    universityName: value => value.trim() === "" || value.trim().length >= 2 || "University name is too short",
    academicYear: value => value.trim() === "" || /^[0-9]+(st|nd|rd|th)\sYear$/i.test(value) || "Format example: '1st Year'",
    stream: value => value.trim() === "" || value.trim().length >= 2 || "Stream must be at least 2 characters"
};

    function showError(input, message) {
        let errorDiv = input.parentElement.querySelector(".error-message");
        if (!errorDiv) {
            // Create error container if missing
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

    function validateField(input) {
        const rule = validators[input.name];
        if (!rule) return true; // Optional field
        const value = input.type === "file" ? input.value : input.value.trim();
        const valid = rule(value);
        if (valid !== true) {
            showError(input, valid);
            return false;
        } else {
            showError(input, "");
            return true;
        }
    }

    // Live validation
    form.querySelectorAll("input, select").forEach(input => {
        input.addEventListener("blur", () => validateField(input));
        input.addEventListener("input", () => validateField(input));
    });

    // Step navigation with validation
    document.getElementById('nextButton').addEventListener('click', function () {
        let valid = true;
        document.querySelectorAll('#step1 input, #step1 select').forEach(input => {
            if (!validateField(input)) valid = false;
        });
        if (valid) {
            document.getElementById('step1').style.display = 'none';
            document.getElementById('step2').style.display = 'block';
        }
    });

    document.getElementById('backButton').addEventListener('click', function () {
        document.getElementById('step2').style.display = 'none';
        document.getElementById('step1').style.display = 'block';
    });

    // On final submit validation
    form.addEventListener("submit", function (e) {
        let valid = true;
        form.querySelectorAll("input, select").forEach(input => {
            if (!validateField(input)) valid = false;
        });
        if (!valid) e.preventDefault();
    });

    // File upload display
    document.getElementById('dobProof').addEventListener('change', function (e) {
        const fileName = e.target.files[0] ? e.target.files[0].name : 'No file uploaded';
        this.parentElement.querySelector('.file-name').textContent = fileName;
    });

    document.getElementById('photoUpload').addEventListener('change', function (e) {
        const fileName = e.target.files[0] ? e.target.files[0].name : 'No file uploaded';
        this.parentElement.querySelector('.file-name').textContent = fileName;
    });

    // Floating labels
    document.querySelectorAll('.form-control').forEach(input => {
        if (input.value) {
            input.nextElementSibling.classList.add('active');
        }
        input.addEventListener('focus', function () {
            this.nextElementSibling.classList.add('active');
        });
        input.addEventListener('blur', function () {
            if (!this.value) {
                this.nextElementSibling.classList.remove('active');
            }
        });
    });
});
