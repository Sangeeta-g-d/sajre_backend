// payment.js
document.addEventListener("DOMContentLoaded", function() {
    // Terms agreement and modal handling
    let agreeBtn = document.getElementById("agreeBtn");
    let checkbox = document.getElementById("agreeCheckbox");

    if (agreeBtn) {
        agreeBtn.addEventListener("click", function(e) {
            e.preventDefault();

            if (agreeBtn.dataset.termsAccepted === "true") {
                // Already accepted → just show modal
                var feesModal = new bootstrap.Modal(document.getElementById("feesModal"));
                feesModal.show();
            } else {
                if (!checkbox.checked) {
                    alert("You must agree to continue.");
                    return;
                }

                // Save accepted_terms
                fetch(agreeBtn.dataset.termsUrl, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": agreeBtn.dataset.csrfToken,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ accepted_terms: true })
                }).then(res => res.json())
                .then(data => {
                    if (data.status === "success") {
                        var feesModal = new bootstrap.Modal(document.getElementById("feesModal"));
                        feesModal.show();
                    } else {
                        alert("Error: " + data.message);
                    }
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

            // Create order from backend
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
                            // Handle successful payment
                            window.location.href = payBtn.dataset.successUrl + "?payment_id=" + response.razorpay_payment_id;
                        },
                        "prefill": {
                            "name": payBtn.dataset.userName,
                            "email": payBtn.dataset.userEmail,
                            "contact": payBtn.dataset.userPhone
                        },
                        "theme": {
                            "color": "#667eea"
                        }
                    };

                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                } else {
                    alert("Error creating order: " + data.message);
                }
            });
        });
    }

    // Auto-open modal if terms already accepted
    if (document.body.dataset.termsAccepted === "true") {
        var feesModal = new bootstrap.Modal(document.getElementById("feesModal"));
        feesModal.show();
    }
});