
        import { DotLottie } from "https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web/+esm";

        // Initialize Lottie animation
        new DotLottie({
            autoplay: true,
            loop: true,
            canvas: document.getElementById("lottie-canvas"),
            src: "https://lottie.host/1197e7ab-7b58-48f7-86e9-6706d1dc8756/ly3NSmJS9W.lottie",
        });

        // Form step navigation
        document.getElementById('nextButton').addEventListener('click', function () {
            document.getElementById('step1').style.display = 'none';
            document.getElementById('step2').style.display = 'block';
        });

        document.getElementById('backButton').addEventListener('click', function () {
            document.getElementById('step2').style.display = 'none';
            document.getElementById('step1').style.display = 'block';
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

        // Initialize floating labels
        document.querySelectorAll('.form-control').forEach(input => {
            // Set initial state
            if (input.value) {
                input.nextElementSibling.classList.add('active');
            }

            // Add event listeners
            input.addEventListener('focus', function () {
                this.nextElementSibling.classList.add('active');
            });

            input.addEventListener('blur', function () {
                if (!this.value) {
                    this.nextElementSibling.classList.remove('active');
                }
            });
        });
