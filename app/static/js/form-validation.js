document.getElementById('signup-form').addEventListener('submit', function (e) {
  e.preventDefault();

  // Collect form data into a JSON object
  const formData = {
    firstName: document.getElementById('first_name').value,
    lastName: document.getElementById('last_name').value,
    userName: document.getElementById('username').value,
    userEmail: document.getElementById('email').value,
    userPassword: document.getElementById('password').value,
    confirmPassword: document.getElementById('confirmpassword').value
  };

  // check if both passwords match
  function checkPasswords () {
    const userPassword = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmpassword').value;
    const passwordError = document.getElementById('confirmPassword-error');
    const passwordI = document.getElementById('confirmpassword'); // get id of password input

    if (userPassword !== confirmPassword) {
      passwordError.textContent = 'Password does not match';
      passwordI.style.marginBottom = 0;
    }
  }

  checkPasswords();

  // Validate Password
  const passwordE = document.querySelector('#password');
  // Get the error Element
  const errorMessage = document.querySelector('#password-error');

  const validatePassword = () => {
    let valid = false;
    const password = passwordE.value.trim();

    if (!isRequired(password)) {
      blankError();
    } else if (!isPasswordSecure(password)) {
      showError();
    } else {
      showSuccess();
      valid = true;
    }
    return valid;
  };

  const isPasswordSecure = (password) => {
    const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})/;
    return re.test(password);
  };

  const showError = () => {
    errorMessage.textContent = 'Password must be at least 8 characters including-[a-z],[A-Z],[0-9],[!@#$%^&*]';
    passwordE.style.marginBottom = 0;
  };

  const blankError = () => {
    errorMessage.textContent = 'Password cannot be blank';
    passwordE.style.marginBottom = 0;
  };

  const showSuccess = () => {
    errorMessage.textContent = '';
  };

  const isRequired = (value) => value !== '';

  if (!validatePassword()) {
    // Password is not valid, do not submit the form
    return;
  }

  // Validate Email
  const emailE = document.querySelector('#email');

  // get the error element
  const errorMessageE = document.querySelector('#email-error');

  const validateEmail = () => {
    let valid = false;

    const email = emailE.value.trim();

    if (!isRequiredE(email)) {
      blankErrorE();
    } else if (!isEmailValid(email)) {
      showErrorE();
    } else {
      showSuccessE();
      valid = true;
    }
    return valid;
  };

  const isRequiredE = (value) => value !== '';

  const isEmailValid = (email) => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  };

  const blankErrorE = () => {
    errorMessageE.textContent = 'Email cannot be blank';
    emailE.style.marginBottom = 0;
  };

  const showErrorE = () => {
    errorMessageE.textContent = 'Please enter a valid email address';
    emailE.style.marginBottom = 0;
  };

  const showSuccessE = () => {
    errorMessageE.textContent = '';
  };

  if (!validateEmail()) {
    // Email is not valid, do not submit the form
    return;
  }
  // function to check if username or email already exist
  function displayError (response) {
    const userT = document.getElementById('username');
    const emailT = document.getElementById('email');
    const userNameError = document.getElementById('username-error');
    const emailError = document.getElementById('email-error');

    // filter the response and display error message
    if (response.userName) {
      userNameError.textContent = response.userName;
      userT.style.marginBottom = 0;
    } else {
      userNameError.textContent = '';
    }

    if (response.userEmail) {
      emailError.textContent = response.userEmail;
      emailT.style.marginBottom = 0;
    } else {
      emailError.textContent = '';
    }
  }

  // Send data to Flask API using Fetch
  fetch('/submit-data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  })
    .then(response => response.json())
    .then(data => {
      displayError(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
