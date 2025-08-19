document.addEventListener("DOMContentLoaded", function() {
    // Terms agreement and modal handling
    let agreeBtn = document.getElementById("agreeBtn");
    let checkbox = document.getElementById("agreeCheckbox");

    function showToast(message, type="success") {
        let bgColor = type === "success"
            ? "linear-gradient(to right, #00b09b, #96c93d)"
            : "linear-gradient(to right, #ff5f6d, #ffc371)";

        Toastify({
            text: message,
            duration: 3000,
            close: true,
            gravity: "top",
            position: "right",
            backgroundColor: bgColor,
            stopOnFocus: true,
        }).showToast();
    }

    if (agreeBtn) {
        agreeBtn.addEventListener("click", function(e) {
            e.preventDefault();

            const hasAccepted = agreeBtn.dataset.termsAccepted === "true";

            if (hasAccepted) {
                // Already accepted → just show modal
                var feesModal = new bootstrap.Modal(document.getElementById("feesModal"));
                feesModal.show();
            } else {
                if (!checkbox.checked) {
                    showToast("You must agree to continue.", "error");
                    return;
                }

                // Save accepted_terms
                fetch(agreeBtn.dataset.termsUrl, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": agreeBtn.dataset.csrfToken,
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest"    // ✅ required by Django view
                    },
                    body: JSON.stringify({ accepted_terms: true })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "success") {
                        showToast("Terms accepted successfully!", "success");
                        // Show fees modal
                        var feesModal = new bootstrap.Modal(document.getElementById("feesModal"));
                        feesModal.show();
                    } else {
                        showToast("Error: " + data.message, "error");
                    }
                })
                .catch(err => {
                    showToast("Error: " + err, "error");
                });
            }
        });
    }

    // Payment button handling
    let payBtn = document.querySelector(".btn.btn-primary");
    
    if (payBtn) {
        payBtn.addEventListener("click", function() {
            let totalAmount = payBtn.dataset.totalAmount;
            let amountInPaisa = Math.round(parseFloat(totalAmount) * 100);

            fetch(payBtn.dataset.createOrderUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": payBtn.dataset.csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "amount=" + amountInPaisa
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "success") {
                    var options = {
                        "key": payBtn.dataset.razorpayKey,
                        "amount": data.order.amount,
                        "currency": "INR",
                        "name": "NAS Competition",
                        "description": "Competition Fee Payment",
                        "order_id": data.order.id,
                        "handler": function(response) {
                            window.location.href = payBtn.dataset.successUrl + "?payment_id=" + response.razorpay_payment_id;
                        },
                        "prefill": {
                            "name": payBtn.dataset.userName,
                            "email": payBtn.dataset.userEmail,
                            "contact": payBtn.dataset.userPhone
                        },
                        "theme": { "color": "#667eea" }
                    };

                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                } else {
                    showToast("Error creating order: " + data.message, "error");
                }
            }).catch(err => {
                showToast("Error: " + err, "error");
            });
        });
    }

    // Auto-open modal if terms already accepted
    if (document.body.dataset.termsAccepted === "true") {
        var feesModal = new bootstrap.Modal(document.getElementById("feesModal"));
        feesModal.show();
    }
});
