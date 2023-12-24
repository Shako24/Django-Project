const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const phone = document.getElementById('id_phone_number_1');
const pass = document.getElementById('id_password');
const email = document.getElementById('id_email');
const username = document.getElementById('id_username');
const pass1 = document.getElementById('id_password1');
const pass2 = document.getElementById('id_password2');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

// Changing placeholder fields for Django Forms
username.placeholder = "Username";
email.placeholder = 'Email';
pass.placeholder = 'Password';
pass1.placeholder = 'Enter new Password';
pass2.placeholder = 'Re-type your Password';