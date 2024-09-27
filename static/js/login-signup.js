// Function to handle form submission for Signup
async function handleSignup(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    // Get form values
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm-password').value;

    // Basic form validation
    if (!username || !email || !password || !confirmPassword) {
        alert('Please fill in all fields');
        return;
    }
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    // Prepare the data to send to the backend
    const data = {
        username: username,
        email: email,
        password: password,
        confirm_password: confirmPassword
    };

    // Send data to the server using POST request
    try {
        const response = await fetch('/home/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.status === 201) {
            alert('Signup successful!');
            window.location.href = '/home/login';  // Redirect to login page
        } else {
            alert(result.error || 'Signup failed. Please try again.');
        }
    } catch (error) {
        console.error('Error during signup:', error);
        alert('An error occurred during signup.');
    }
}

// Function to handle form submission for Login
async function handleLogin(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    // Get form values
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    // Basic form validation
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }

    // Prepare the data to send to the backend
    const data = {
        email: email,
        password: password
    };

    // Send data to the server using POST request
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.status === 200) {
            alert('Login successful!');
            window.location.href = '/dashboard';  // Redirect to the dashboard after successful login
        } else {
            alert(result.error || 'Login failed. Please try again.');
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login.');
    }
}

// Attach event listeners to signup and login buttons
document.getElementById('signup-form').addEventListener('submit', handleSignup);
document.getElementById('login-form').addEventListener('submit', handleLogin);
