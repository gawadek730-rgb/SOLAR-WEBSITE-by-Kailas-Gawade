// ===============================
// MOBILE MENU TOGGLE
// ===============================
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');
const menuIcon = document.getElementById('menuIcon');

mobileMenuBtn.addEventListener('click', () => {
    navMenu.classList.toggle('active');

    if (navMenu.classList.contains('active')) {
        menuIcon.classList.remove('fa-bars');
        menuIcon.classList.add('fa-times');
    } else {
        menuIcon.classList.remove('fa-times');
        menuIcon.classList.add('fa-bars');
    }
});


// ===============================
// POPUP OPEN & CLOSE
// ===============================
function showForm() {
    document.getElementById("quotePopup").style.display = "flex";
}

function closeForm() {
    document.getElementById("quotePopup").style.display = "none";
}


// ===============================
// GOOGLE SHEET FORM SUBMISSION
// ===============================
document.getElementById("floatingQuoteForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const message = document.getElementById("formMessage");

    // Show loading message immediately
    message.innerHTML = "⏳ Submitting...";
    message.style.color = "orange";
    message.style.display = "block";

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        city: document.getElementById("city").value,
        solarType: document.getElementById("solarType").value
    };

    fetch("https://script.google.com/macros/s/AKfycbwwt05dxW0CGERIIBxpAW4Sgg6-MBfPbWLExOfiO8k9615jJSKxXnVJ8DVfiYdmFc1L/exec", {
        method: "POST",
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {

            if (response.result === "success") {

                message.innerHTML = "✅ Form Submitted Successfully!";
                message.style.color = "green";

                document.getElementById("floatingQuoteForm").reset();

                setTimeout(() => {
                    closeForm();
                    message.style.display = "none";
                }, 2000);

            } else {
                message.innerHTML = "❌ Submission Failed!";
                message.style.color = "red";
            }

        })
        .catch(error => {
            message.innerHTML = "❌ Error submitting form!";
            message.style.color = "red";
            console.error(error);
        });

});