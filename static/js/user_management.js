document.addEventListener('DOMContentLoaded', function() {

    set_form_validation();

    // Set validation for settings forms
    const account_settings_forms = document.getElementsByClassName('account-settings-form');
    Array.from(account_settings_forms).forEach(form => {
        form.addEventListener('change', function() {
            form.classList.add('was-changed')
        })
    })
});

async function submit_settings_forms() {

    // Get all changed forms
    const forms = document.getElementsByClassName('was-changed');

    if (!forms.length) {
        // In case no form was changed
        return;
    }
    for await (const form of forms) {
        if (form.id === 'main-info-form') {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source main info
                if (!await update_user_main_info(form)) {
                    // Error case
                    return location.reload()
                }
            }
        }
        else if (form.id === 'change-password-form') {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source link
                if (!await change_user_password(form)) {
                    // Error case
                    return location.reload()
                }
            }
        }
    }
    return window.location.replace('/login')
}

async function update_user_main_info(form) {

    // Account settings view
    const url = '/account_settings';

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return false;
        }
    })
}

async function change_user_password(form) {

    // Account settings view
    const url = '/change_password';

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return false;
        }
    })
}

function change_forms() {
    
    // Get both forms
    let first_form = document.querySelector('#first_form');
    let second_form = document.querySelector('#second_form');

    // Hide one and show other
    if (second_form.style.display === 'none') {
        first_form.style.display = 'none';
        second_form.style.display = 'block';
    }
    else {
        second_form.style.display = 'none';
        first_form.style.display = 'block';
    }
}

function check_password(form_name) {

    // Get new password and its confirmation
    const password = document.forms[form_name]["password"].value;
    const confirmation = document.forms[form_name]["confirmation"].value;
    const length = password.length;
    let digit = false;
    let upper = false;

    // Show error message if password and confirmation don't match
    if (password != confirmation) {

        console.log("password and confirmation don't match");
        return false;
        // TODO Swal.Fire error message
    }

    for (let i = 0; i < length; i++) {

        let char = password[i];

        // Check if at least one character is digit
        if (char >= '0' && char <= '9') {

            digit = true;
        }
        // Check if at least one character is uppercase
        else if (char === char.toUpperCase()) {

            upper = true;
        }
    }

    if (!(digit && upper && length > 5)) {

        // TODO
        console.log('sorry')
        return false;
    }

    // Submit the form if password is ok
    return true;
}


function set_form_validation() {

    // Fetch all the forms
    const forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })
}
