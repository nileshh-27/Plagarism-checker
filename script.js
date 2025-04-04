document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match. Please try again.");
    } else {
        alert("Sign Up Successful!"); // Here you would typically send the data to the server
        this.submit(); // You can uncomment this line to proceed with form submission
    }
});
    document.getElementById("signupForm").addEventListener("submit", function(event) {
        event.preventDefault();
        
        const username = document.getElementById("username").value;
        localStorage.setItem("username", username); // Store username in local storage

        window.location.href = "plaggearly.html"; // Redirect to plaggearly.html
    });

