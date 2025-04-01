document.addEventListener("DOMNodeInserted", function () {
    let modalTitle = document.querySelector(".modal-title.text-break");
    if (modalTitle && modalTitle.textContent.trim() === "Odoo") {
        modalTitle.innerHTML = "<b>LMS</b>";
    }
});

document.addEventListener("DOMNodeInserted", function () {
    let passwordPrompt = document.querySelector(".o_form_sheet_bg h3 strong");
    if (passwordPrompt && passwordPrompt.textContent.trim() === "Please enter your password to confirm you own this account") {
        passwordPrompt.textContent = "Please enter your old password to confirm your account";
    }
});


document.addEventListener("DOMNodeInserted", function () {
    let passwordError = document.querySelector(".text-prewrap");
    if (passwordError && passwordError.textContent.trim() === "Incorrect Password, try again or click on Forgot Password to reset your password.") {
        passwordError.textContent = "Incorrect Password, please try again your old password.";
    }
});



document.addEventListener("DOMNodeInserted", function () {
    let passwordInput = document.querySelector(".o_input#password_0");
    if (passwordInput && passwordInput.placeholder.trim() === "************") {
        passwordInput.placeholder = "Enter Your Password";
    }
});


document.addEventListener("DOMNodeInserted", function () {
    let passwordMismatch = document.querySelector(".text-prewrap");
    if (passwordMismatch && passwordMismatch.textContent.trim() === "The new password and its confirmation must be identical.") {
        passwordMismatch.textContent = "New password and confirmation password must be identical";
    }
});

document.addEventListener("DOMNodeInserted", function () {
    let forgotPasswordLink = document.querySelector('a[href="/web/reset_password/"]');
    if (forgotPasswordLink) {
        forgotPasswordLink.style.display = "none";
    }
});


