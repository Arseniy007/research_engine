document.addEventListener('DOMContentLoaded', function() {

    const show_form_buttons = document.getElementsByClassName('show_form_button');
    const number_of_buttons = show_form_buttons.length;
    
    for (let i = 0; i < number_of_buttons; i++) {
        let button = show_form_buttons[i];
        button.addEventListener('click', () => show_and_hide_forms(`${button.id}_form`));
    }

    console.log("hus");


});



function show_and_hide_forms(form_id) {

    let all_forms = document.querySelector('.source_form');
    const number_of_forms = all_forms.length;

    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }

    document.querySelector(`#${form_id}`).style.display = 'block';

};


function hide_all_forms() {

    let all_forms = document.querySelector('.source_form');
    const number_of_forms = all_forms.length;
    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }
}