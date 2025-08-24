// static/assets/mentor/js/vendor-profile-validation.js

// Helper functions for error handling
function showError(input, message) {
    const errorDiv = input.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
    input.classList.add("is-invalid");
}

function clearError(input) {
    const errorDiv = input.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.textContent = "";
        errorDiv.style.display = 'none';
    }
    input.classList.remove("is-invalid");
}

// Validation functions
function validateTextField(input) {
    const regex = /^[A-Za-z\s.,'-]+$/;
    if (input.value.trim() !== "" && !regex.test(input.value.trim())) {
        showError(input, "Only alphabets, spaces, and basic punctuation are allowed.");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function validateNumberField(input) {
    if (input.value && isNaN(input.value)) {
        showError(input, "Please enter a valid number.");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function validatePincode(input) {
    const regex = /^\d{6}$/;
    if (input.value && !regex.test(input.value)) {
        showError(input, "PIN code must be exactly 6 digits.");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function validateExperience(input) {
    // Allow empty values for optional fields
    if (input.value.trim() === '') {
        clearError(input);
        return true;
    }
    
    const value = parseFloat(input.value);
    if (isNaN(value) || value < 0 || value > 50) {
        showError(input, "Please enter a valid experience between 0 and 50 years.");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function validateFile(input, maxSize, fileTypes) {
    if (input.files.length > 0) {
        const file = input.files[0];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        // Check file size
        if (file.size > maxSize) {
            showError(input, `File must be less than ${maxSize / (1024*1024)}MB.`);
            return false;
        }
        
        // Check file type
        if (fileTypes && !fileTypes.includes(fileExtension) && !fileTypes.includes(file.type)) {
            showError(input, `Please upload a valid file type: ${fileTypes.join(', ')}.`);
            return false;
        }
        
        clearError(input);
        return true;
    }
    return true; // No file is not an error until required validation
}

// Set up event listeners for real-time validation
function setupFormValidation() {
    // Text fields validation on input
    const textFields = ['full_name', 'city', 'district', 'state', 'store_or_advisor', 
                       'job_title', 'current_employer', 'location', 'course_level', 'course_name'];
    
    textFields.forEach(fieldId => {
        const input = document.getElementById(fieldId);
        if (input) {
            input.addEventListener('input', function() {
                validateTextField(this);
            });
            
            input.addEventListener('blur', function() {
                validateTextField(this);
            });
        }
    });
    
    // Number fields validation
    const experienceField = document.getElementById('total_experience_years');
    if (experienceField) {
        experienceField.addEventListener('input', function() {
            validateExperience(this);
        });
    }
    
    const pincodeField = document.getElementById('pincode');
    if (pincodeField) {
        pincodeField.addEventListener('input', function() {
            validatePincode(this);
        });
    }
    
    // File upload validation on change
    document.querySelectorAll('.file-input').forEach(input => {
        input.addEventListener('change', function() {
            const fileTypes = this.id === 'passport_photo' 
                ? ['jpg', 'jpeg', 'png', 'gif'] 
                : ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'];
            const maxSize = this.id === 'passport_photo' 
                ? 2 * 1024 * 1024 
                : 5 * 1024 * 1024;
                
            validateFile(this, maxSize, fileTypes);
            
            // Update file name display
            const fileNameDiv = this.parentElement.querySelector('.file-name');
            if (fileNameDiv && this.files.length > 0) {
                fileNameDiv.textContent = this.files[0].name;
            }
        });
    });
    
    // Select field validation
    const qualificationSelect = document.getElementById('higherQualification');
    if (qualificationSelect) {
        qualificationSelect.addEventListener('change', function() {
            if (this.value === '') {
                showError(this, "This field is required.");
            } else {
                clearError(this);
            }
        });
    }
    
    // Textarea validation
    const textareas = ['full_address', 'work_history'];
    textareas.forEach(textareaId => {
        const textarea = document.getElementById(textareaId);
        if (textarea) {
            textarea.addEventListener('input', function() {
                if (this.hasAttribute('required') && this.value.trim() === '') {
                    showError(this, "This field is required.");
                } else {
                    clearError(this);
                }
            });
        }
    });
}

// Form submission validation
function validateForm() {
    let valid = true;
    
    // Validate required text fields
    const requiredTextFields = ['full_name', 'city', 'district', 'state'];
    requiredTextFields.forEach(fieldId => {
        const input = document.getElementById(fieldId);
        if (input && input.hasAttribute('required')) {
            if (input.value.trim() === '') {
                showError(input, "This field is required.");
                valid = false;
            } else if (!validateTextField(input)) {
                valid = false;
            }
        }
    });
    
    // Validate pincode
    const pincodeField = document.getElementById('pincode');
    if (pincodeField && pincodeField.hasAttribute('required')) {
        if (pincodeField.value.trim() === '') {
            showError(pincodeField, "This field is required.");
            valid = false;
        } else if (!validatePincode(pincodeField)) {
            valid = false;
        }
    }
    
    // Validate qualification select
    const qualificationSelect = document.getElementById('higherQualification');
    if (qualificationSelect && qualificationSelect.hasAttribute('required')) {
        if (qualificationSelect.value === '') {
            showError(qualificationSelect, "This field is required.");
            valid = false;
        }
    }
    
    // Validate full address textarea
    const fullAddress = document.getElementById('full_address');
    if (fullAddress && fullAddress.hasAttribute('required')) {
        if (fullAddress.value.trim() === '') {
            showError(fullAddress, "This field is required.");
            valid = false;
        }
    }
    
    // Validate experience field if it has value
    const experienceField = document.getElementById('total_experience_years');
    if (experienceField && experienceField.value.trim() !== '') {
        if (!validateExperience(experienceField)) {
            valid = false;
        }
    }
    
    // Validate file uploads
    const passport = document.getElementById("passport_photo");
    if (passport && passport.hasAttribute('required')) {
        if (passport.files.length === 0) {
            showError(passport, "Passport photo is required.");
            valid = false;
        } else if (!validateFile(passport, 2 * 1024 * 1024, ['jpg', 'jpeg', 'png', 'gif'])) {
            valid = false;
        }
    }
    
    const idProof = document.getElementById("id_proof");
    if (idProof && idProof.hasAttribute('required')) {
        if (idProof.files.length === 0) {
            showError(idProof, "ID proof is required.");
            valid = false;
        } else if (!validateFile(idProof, 5 * 1024 * 1024, ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'])) {
            valid = false;
        }
    }
    
    return valid;
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    setupFormValidation();
    
    // Form submission handler
    const form = document.getElementById('mentorRegistrationForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            if (!validateForm()) {
                Toastify({
                    text: "Please fix the errors in the form.",
                    duration: 3000, 
                    close: true,
                    gravity: "top", 
                    backgroundColor: "linear-gradient(to right, #ff5f6d, #ffc371)"
                }).showToast();
                return;
            }

            const formData = new FormData(this);

            fetch(this.action, {
                method: "POST",
                headers: { 
                    "X-CSRFToken": this.querySelector('[name=csrfmiddlewaretoken]').value 
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    Toastify({ 
                        text: data.message, 
                        duration: 3000, 
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)"
                    }).showToast();
                    setTimeout(() => { 
                        // Get the URL from the hidden field
                        const dashboardUrl = document.getElementById('dashboardUrl').value;
                        window.location.href = dashboardUrl; 
                    }, 2000);
                } else {
                    Toastify({
                        text: data.message, 
                        duration: 3000, 
                        close: true,
                        gravity: "top", 
                        backgroundColor: "linear-gradient(to right, #ff5f6d, #ffc371)"
                    }).showToast();
                }
            })
            .catch(error => {
                Toastify({
                    text: "An error occurred. Please try again.",
                    duration: 3000, 
                    close: true,
                    gravity: "top", 
                    backgroundColor: "linear-gradient(to right, #ff5f6d, #ffc371)"
                }).showToast();
            });
        });
    }
});