// API base URL
const API = '';

// Token management
function saveToken(token) {
    localStorage.setItem('agritech_token', token);
}

function getToken() {
    return localStorage.getItem('agritech_token');
}

function clearToken() {
    localStorage.removeItem('agritech_token');
}

// Redirect if already logged in
if (window.location.pathname === '/login' || window.location.pathname === '/') {
    if (getToken()) {
        window.location.href = '/dashboard';
    }
}

// Redirect if not logged in
if (window.location.pathname === '/dashboard') {
    if (!getToken()) {
        window.location.href = '/login';
    }
}

// LOGIN
const loginBtn = document.getElementById('login-btn');
if (loginBtn) {
    loginBtn.addEventListener('click', async () => {
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const errorDiv = document.getElementById('error-message');

        if (!email || !password) {
            errorDiv.textContent = 'Please enter email and password.';
            errorDiv.classList.remove('hidden');
            return;
        }

        try {
            const response = await fetch(`${API}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                saveToken(data.access_token);
                window.location.href = '/dashboard';
            } else {
                errorDiv.textContent = data.detail || 'Login failed.';
                errorDiv.classList.remove('hidden');
            }
        } catch (err) {
            errorDiv.textContent = 'Cannot connect to server.';
            errorDiv.classList.remove('hidden');
        }
    });
}

//REGISTER
const registerBtn = document.getElementById('register-btn');
if (registerBtn) {
  registerBtn.addEventListener('click', async () => {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorDiv = document.getElementById('error-message');

    if (!name || !email || !password) {
      errorDiv.textContent = 'Please enter name, email and password.';
      errorDiv.classList.remove('hidden');
      return;
    }

    try {
      const response = await fetch(`${API}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({name, email, password})
      });

      const data = await response.json();

      if (response.ok) {
//        saveToken(data.access_token); // maybe i should let the user login manually without the system holding the token
        window.location.href = '/login';
      } else {
        errorDiv.textContent = data.detail || 'Registration failed';
        errorDiv.classList.remove('hidden');
     }
    }catch (err) {
      errorDiv.textContent= 'Cannot connect to server.';
      errorDiv.classList.remove('hidden');
    }
  });
}

