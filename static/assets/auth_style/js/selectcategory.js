
document.addEventListener("DOMContentLoaded", function() {
    // Initialize Lottie animation
    new DotLottie({
        autoplay: true,
        loop: true,
        canvas: document.getElementById("lottie-canvas"),
        src: "https://lottie.host/c87b4286-78e8-4812-8bea-a5fc104c5b09/jjZcK4GzdO.lottie",
    });

    // Dropdown functionality
    const dropdownBtn = document.getElementById('dropdownBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const continueBtn = document.getElementById('continueBtn');
    const selectedOption = document.getElementById('selectedOption');
    const roleInput = document.getElementById('roleInput');

    if (dropdownBtn) {
        dropdownBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('show');
            this.classList.toggle('open');
        });
    }

    document.addEventListener('click', function () {
        if (dropdownBtn) dropdownBtn.classList.remove('open');
        if (dropdownMenu) dropdownMenu.classList.remove('show');
    });

    // Category selection
    window.selectCategory = function(category, icon) {
        if (selectedOption) {
            selectedOption.innerHTML = `<span style="margin-right: 8px;">${icon}</span>${category}`;
        }
        if (roleInput) {
            roleInput.value = category;
        }
        if (dropdownBtn) dropdownBtn.classList.remove('open');
        if (dropdownMenu) dropdownMenu.classList.remove('show');
        if (continueBtn) continueBtn.disabled = false;
    };

    // Select element functionality
    const categorySelect = document.getElementById('categorySelect');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const roleInput = document.getElementById('roleInput');
            const continueBtn = document.getElementById('continueBtn');
            
            if (this.value) {
                if (roleInput) roleInput.value = this.value;
                if (continueBtn) continueBtn.disabled = false;
            } else {
                if (continueBtn) continueBtn.disabled = true;
            }
        });
    }
});
