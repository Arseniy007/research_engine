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
