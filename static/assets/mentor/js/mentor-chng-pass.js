

    // Toggle password visibility
    document.getElementById('toggle-password').onclick = function() {
        const input = document.getElementById('new-password');
        const icon = document.getElementById('eye-icon');
        if (input.type === "password") {
            input.type = "text";
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            input.type = "password";
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    };

    // Show correct icon if password meets requirements (example: min 8 chars)
    document.getElementById('new-password').addEventListener('input', function() {
        const validIcon = document.getElementById('password-valid');
        if (this.value.length >= 8) {
            validIcon.style.display = 'inline';
        } else {
            validIcon.style.display = 'none';
        }
    });