document.addEventListener('DOMContentLoaded', function() {
    set_form_validation();
});

function change_forms() {
    
    // Get both forms
    let first_form = document.getElementById('first-form');
    let second_form = document.getElementById('second-form');

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
