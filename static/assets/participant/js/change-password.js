document.addEventListener("DOMContentLoaded", () => {
    // Toggle password visibility
    document.querySelectorAll(".toggle-password").forEach(icon => {
        icon.addEventListener("click", () => {
            const targetId = icon.getAttribute("data-target");
            const input = document.getElementById(targetId);
            const eyeIcon = icon.querySelector("i");

            if (input && eyeIcon) {
                if (input.type === "password") {
                    input.type = "text";
                    eyeIcon.classList.remove("bi-eye");
                    eyeIcon.classList.add("bi-eye-slash");
                } else {
                    input.type = "password";
                    eyeIcon.classList.remove("bi-eye-slash");
                    eyeIcon.classList.add("bi-eye");
                }
            }
        });
    });

    // Password validation
    const newPassword = document.getElementById("new-password");
    const confirmPassword = document.getElementById("confirm-password");
    const submitBtn = document.querySelector(".btn-confirm");

    function validatePassword() {
        const value = newPassword.value;

        document.getElementById("lowercase").className = /[a-z]/.test(value) ? "valid" : "invalid";
        document.getElementById("uppercase").className = /[A-Z]/.test(value) ? "valid" : "invalid";
        document.getElementById("number").className = /\d/.test(value) ? "valid" : "invalid";
        document.getElementById("special").className = /[!@#$%^&*(),.?\":{}|<>]/.test(value) ? "valid" : "invalid";
        document.getElementById("length").className = value.length >= 8 ? "valid" : "invalid";

        const match = value && confirmPassword.value && value === confirmPassword.value;
        document.getElementById("match").className = match ? "valid" : "invalid";

        // ✅ Enable submit only if all requirements are valid
        const allValid = [...document.querySelectorAll(".checklist li")]
            .every(item => item.classList.contains("valid"));

        submitBtn.disabled = !allValid;
    }

    if (newPassword && confirmPassword) {
        newPassword.addEventListener("input", validatePassword);
        confirmPassword.addEventListener("input", validatePassword);
    }

    // Initially disable submit
    if (submitBtn) submitBtn.disabled = true;
});
