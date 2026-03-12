// ===============================
// MOBILE MENU TOGGLE
// ===============================
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');
const menuIcon = document.getElementById('menuIcon');

if (mobileMenuBtn && navMenu && menuIcon) {

    mobileMenuBtn.addEventListener('click', () => {

        navMenu.classList.toggle('active');

        if (navMenu.classList.contains('active')) {
            menuIcon.classList.replace('fa-bars', 'fa-times');
        } else {
            menuIcon.classList.replace('fa-times', 'fa-bars');
        }

    });

}


// ===============================
// QUOTE POPUP OPEN & CLOSE
// ===============================
function showForm() {
    const popup = document.getElementById("quotePopup");
    if (popup) popup.style.display = "flex";
}

function closeForm() {
    const popup = document.getElementById("quotePopup");
    if (popup) popup.style.display = "none";
}


// ===============================
// SOLAR CALCULATOR POPUP
// ===============================
function openCalculator() {
    const calc = document.getElementById("calculatorPopup");
    if (calc) calc.style.display = "flex";
}

function closeCalculator() {
    const calc = document.getElementById("calculatorPopup");
    if (calc) calc.style.display = "none";
}


// ===============================
// SOLAR CALCULATOR LOGIC
// ===============================
function solarCalc() {

    const billInput = document.getElementById("bill");
    const rateInput = document.getElementById("rate");
    const result = document.getElementById("result");

    if (!billInput || !rateInput || !result) return;

    const bill = parseFloat(billInput.value);
    const rate = parseFloat(rateInput.value);

    if (!bill || !rate || rate === 0) {
        result.innerHTML = "<p>Please enter valid values.</p>";
        return;
    }

    const units = bill / rate;
    const system = units / 120;
    const cost = system * 55000;

    result.innerHTML = `
        <p><b>Monthly Units:</b> ${units.toFixed(0)}</p>
        <p><b>Recommended System:</b> ${system.toFixed(2)} kW</p>
        <p><b>Estimated Cost:</b> ₹${cost.toFixed(0)}</p>
    `;
}


// ===============================
// GOOGLE SHEET FORM SUBMISSION
// ===============================
const quoteForm = document.getElementById("floatingQuoteForm");

if (quoteForm) {

    quoteForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        const message = document.getElementById("formMessage");

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

        try {

            const res = await fetch("https://script.google.com/macros/s/AKfycbwwt05dxW0CGERIIBxpAW4Sgg6-MBfPbWLExOfiO8k9615jJSKxXnVJ8DVfiYdmFc1L/exec", {
                method: "POST",
                body: JSON.stringify(data)
            });

            const response = await res.json();

            if (response.result === "success") {

                alert("✅ Quote Request Submitted Successfully!");

                message.innerHTML = "Submitted Successfully!";
                message.style.color = "green";

                quoteForm.reset();

                setTimeout(() => {
                    closeForm();
                    message.style.display = "none";
                }, 3000);

            } else {

                alert("❌ Quote submission failed!");
                message.innerHTML = "Submission Failed!";
                message.style.color = "red";

            }

        } catch (error) {

            alert("❌ Error submitting form!");
            console.error(error);

        }

    });

}


// ===============================
// CAREER POPUP
// ===============================
function openCareerForm(position) {

    const popup = document.getElementById("careerForm");
    const jobField = document.getElementById("jobPosition");

    if (popup) popup.style.display = "flex";
    if (jobField) jobField.value = position;

}

function closeCareerForm() {

    const popup = document.getElementById("careerForm");
    if (popup) popup.style.display = "none";

}


// ===============================
// CLOSE POPUP WHEN CLICK OUTSIDE
// ===============================
window.onclick = function (event) {

    const quotePopup = document.getElementById("quotePopup");
    const careerPopup = document.getElementById("careerForm");
    const calcPopup = document.getElementById("calculatorPopup");

    if (event.target === quotePopup) quotePopup.style.display = "none";
    if (event.target === careerPopup) careerPopup.style.display = "none";
    if (event.target === calcPopup) calcPopup.style.display = "none";

};


// ===============================
// CAREER FORM SUBMIT (MONGODB)
// ===============================
const careerApplyForm = document.getElementById("careerApplyForm");

if (careerApplyForm) {

    careerApplyForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        const submitBtn = careerApplyForm.querySelector("button");

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerText = "Submitting...";
        }

        const formData = new FormData(careerApplyForm);

        try {

            const response = await fetch("http://127.0.0.1:5000/apply", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (result.status === "success") {

                alert("✅ Application Submitted Successfully!");

                careerApplyForm.reset();

                setTimeout(() => {

                    closeCareerForm();

                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerText = "Submit Application";
                    }

                }, 2000);

            } else {

                alert("❌ Application Submission Failed!");

                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerText = "Submit Application";
                }

            }

        } catch (error) {

            alert("❌ Server Error! Please try again.");

            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerText = "Submit Application";
            }

            console.error(error);

        }

    });

}