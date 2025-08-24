// vendor-profile-validation.js

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
    // Allow empty values for optional fields
    if (!input.hasAttribute('required') && input.value.trim() === '') {
        clearError(input);
        return true;
    }
    
    const regex = /^[A-Za-z\s.,'-]+$/;
    if (input.value.trim() !== "" && !regex.test(input.value.trim())) {
        showError(input, "Only alphabets, spaces, and basic punctuation are allowed.");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function validateEmail(input) {
    // Allow empty values for optional fields
    if (!input.hasAttribute('required') && input.value.trim() === '') {
        clearError(input);
        return true;
    }
    
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (input.value.trim() !== "" && !regex.test(input.value.trim())) {
        showError(input, "Please enter a valid email address.");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function validatePhone(input) {
    // Allow empty values for optional fields
    if (!input.hasAttribute('required') && input.value.trim() === '') {
        clearError(input);
        return true;
    }
    
    const regex = /^[0-9]{10}$/;
    if (input.value.trim() !== "" && !regex.test(input.value.trim())) {
        showError(input, "Please enter a valid 10-digit phone number.");
        return false;
    } else {
        clearError(input);
        return true;
    }
}

function validateNumberField(input) {
    // Allow empty values for optional fields
    if (!input.hasAttribute('required') && input.value.trim() === '') {
        clearError(input);
        return true;
    }
    
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
    
    // Check if file is required but not uploaded
    if (input.hasAttribute('required') && input.files.length === 0) {
        showError(input, "This file is required.");
        return false;
    }
    
    return true;
}

// Set up event listeners for real-time validation
function setupFormValidation() {
    // Text-only fields validation on input
    document.querySelectorAll('input[type="text"]').forEach(input => {
        // Skip phone and pincode fields
        if (input.id !== 'phone_number' && input.id !== 'pincode') {
            input.addEventListener('input', function() {
                validateTextField(this);
            });
            
            input.addEventListener('blur', function() {
                validateTextField(this);
            });
        }
        
        // Validate on initial load if required
        if (input.hasAttribute('required') && input.value.trim() === '') {
            showError(input, "This field is required.");
        }
    });
    
    // Email field validation
    const emailField = document.getElementById('email');
    if (emailField) {
        emailField.addEventListener('input', function() {
            validateEmail(this);
        });
        
        emailField.addEventListener('blur', function() {
            validateEmail(this);
        });
    }
    
    // Phone field validation
    const phoneField = document.getElementById('phone_number');
    if (phoneField) {
        phoneField.addEventListener('input', function() {
            validatePhone(this);
        });
        
        phoneField.addEventListener('blur', function() {
            validatePhone(this);
        });
        
        // Validate on initial load if required
        if (phoneField.hasAttribute('required') && phoneField.value.trim() === '') {
            showError(phoneField, "This field is required.");
        }
    }
    
    // Pincode field validation
    const pincodeField = document.getElementById('pincode');
    if (pincodeField) {
        pincodeField.addEventListener('input', function() {
            validatePincode(this);
        });
        
        pincodeField.addEventListener('blur', function() {
            validatePincode(this);
        });
        
        // Validate on initial load if required
        if (pincodeField.hasAttribute('required') && pincodeField.value.trim() === '') {
            showError(pincodeField, "This field is required.");
        }
    }
    
    // Experience field validation
    const experienceField = document.getElementById('total_experience_years');
    if (experienceField) {
        experienceField.addEventListener('input', function() {
            validateExperience(this);
        });
        
        experienceField.addEventListener('blur', function() {
            validateExperience(this);
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
        });
    });
    
    // Select field validation
    document.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', function() {
            if (this.hasAttribute('required') && this.value === '') {
                showError(this, "This field is required.");
            } else {
                clearError(this);
            }
        });
        
        // Validate on initial load if required
        if (select.hasAttribute('required') && select.value === '') {
            showError(select, "This field is required.");
        }
    });
    
    // Textarea validation
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            if (this.hasAttribute('required') && this.value.trim() === '') {
                showError(this, "This field is required.");
            } else {
                clearError(this);
            }
        });
        
        // Validate on initial load if required
        if (textarea.hasAttribute('required') && textarea.value.trim() === '') {
            showError(textarea, "This field is required.");
        }
    });
}

// Form submission validation
function validateForm() {
    let valid = true;
    
    // Clear all errors first
    document.querySelectorAll('.error-message').forEach(error => {
        error.textContent = "";
        error.style.display = 'none';
    });
    document.querySelectorAll('.is-invalid').forEach(input => {
        input.classList.remove("is-invalid");
    });
    
    // Validate required text fields
    document.querySelectorAll('input[type="text"][required]').forEach(input => {
        // Skip phone and pincode fields (handled separately)
        if (input.id !== 'phone_number' && input.id !== 'pincode') {
            if (input.value.trim() === '') {
                showError(input, "This field is required.");
                valid = false;
            } else if (!validateTextField(input)) {
                valid = false;
            }
        }
    });
    
    // Validate optional text fields (if they have content)
    document.querySelectorAll('input[type="text"]:not([required])').forEach(input => {
        // Skip phone and pincode fields
        if (input.id !== 'phone_number' && input.id !== 'pincode' && input.value.trim() !== '') {
            if (!validateTextField(input)) {
                valid = false;
            }
        }
    });
    
    // Validate email (readonly but should still be valid)
    const emailField = document.getElementById('email');
    if (emailField && !validateEmail(emailField)) {
        valid = false;
    }
    
    // Validate phone (required)
    const phoneField = document.getElementById('phone_number');
    if (phoneField) {
        if (phoneField.hasAttribute('required') && phoneField.value.trim() === '') {
            showError(phoneField, "This field is required.");
            valid = false;
        } else if (phoneField.value.trim() !== '' && !validatePhone(phoneField)) {
            valid = false;
        }
    }
    
    // Validate pincode (required)
    const pincodeField = document.getElementById('pincode');
    if (pincodeField) {
        if (pincodeField.value.trim() === '') {
            showError(pincodeField, "This field is required.");
            valid = false;
        } else if (!validatePincode(pincodeField)) {
            valid = false;
        }
    }
    
    // Validate experience field (optional)
    const experienceField = document.getElementById('total_experience_years');
    if (experienceField && experienceField.value.trim() !== '') {
        if (!validateExperience(experienceField)) {
            valid = false;
        }
    }
    
    // Validate select field (required)
    const qualificationSelect = document.getElementById('higher_qualification');
    if (qualificationSelect && qualificationSelect.hasAttribute('required')) {
        if (qualificationSelect.value === '') {
            showError(qualificationSelect, "This field is required.");
            valid = false;
        }
    }
    
    // Validate textarea (required)
    const fullAddress = document.getElementById('full_address');
    if (fullAddress && fullAddress.hasAttribute('required')) {
        if (fullAddress.value.trim() === '') {
            showError(fullAddress, "This field is required.");
            valid = false;
        }
    }
    
    // Validate file uploads (optional for edit)
    const passport = document.getElementById("passport_photo");
    if (passport && passport.files.length > 0 && !validateFile(passport, 2 * 1024 * 1024, ['jpg', 'jpeg', 'png', 'gif'])) {
        valid = false;
    }
    
    const idProof = document.getElementById("id_proof");
    if (idProof && idProof.files.length > 0 && !validateFile(idProof, 5 * 1024 * 1024, ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'])) {
        valid = false;
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
                    position: "right",
                    backgroundColor: "linear-gradient(to right, #ff5f6d, #ffc371)"
                }).showToast();
                
                // Scroll to first error
                const firstError = document.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }

            const formData = new FormData(this);

            // Show loading state
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = "Updating Profile...";
            submitButton.disabled = true;

            fetch(this.action, {
                method: "POST",
                headers: { 
                    "X-CSRFToken": this.querySelector('[name=csrfmiddlewaretoken]').value,
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    Toastify({ 
                        text: data.message, 
                        duration: 3000, 
                        close: true,
                        gravity: "top", 
                        position: "right",
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)"
                    }).showToast();
                    
                    // Redirect after successful update
                    setTimeout(() => { 
                        window.location.href = "/vendor/vendor_dashboard/";
                    }, 2000);
                } else {
                    throw new Error(data.message);
                }
            })
            .catch(error => {
                Toastify({
                    text: error.message || "An error occurred. Please try again.",
                    duration: 5000, 
                    close: true,
                    gravity: "top", 
                    position: "right",
                    backgroundColor: "linear-gradient(to right, #ff5f6d, #ffc371)"
                }).showToast();
                console.error('Error:', error);
            })
            .finally(() => {
                // Restore button state
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });
    }
    
    // Cancel button functionality
    const cancelButton = document.querySelector('.btn-cancel');
    if (cancelButton) {
        cancelButton.addEventListener('click', function() {
            window.location.href = "/vendor/vendor_dashboard/";
        });
    }
});