document.addEventListener('DOMContentLoaded', function() {

    const show_form_buttons = document.getElementsByClassName('show_form_button');
    const number_of_buttons = show_form_buttons.length;
    
    for (let i = 0; i < number_of_buttons; i++) {
        let button = show_form_buttons[i];
        button.addEventListener('click', () => show_and_load_form(`${button.id}_form`));
    }

    const forms = document.getElementsByClassName('source_form');
    const number_of_forms = forms.length;

    for (let i = 0; i < number_of_forms; i++) {
        forms[i].addEventListener('submit', () => {
            count_and_set_authors_number(forms[i])
        })
    }
});


function show_and_load_form(form_id) {

    // Hide all forms and show the one that user clicked on
    hide_all_forms();
    let form = document.querySelector(`#${form_id}`);
    form.style.display = 'block';

    // Set number of authors to 1
    let number_of_authors = 0;

    const author_div = form.querySelector('.author_div');
    author_div.innerHTML = create_author_fields(number_of_authors);

    load_new_fields(author_div, number_of_authors);
    
}

function load_new_fields (author_div, author_number) {

    const add_author_button = author_div.querySelector(`#add_author_button_${author_number}`);
    const delete_author_button = author_div.querySelector(`#delete_author_button_${author_number}`);

    if (delete_author_button) {

        delete_author_button.addEventListener('click', function() {

            const author_fields = author_div.querySelector(`#author_fields_${author_number - 1}`);
            console.log(author_fields);
            
            author_fields.remove();
    
        })
    }

    author_number++;

    add_author_button.addEventListener('click', function() {

        const new_fields = document.createElement('div');
        new_fields.innerHTML = create_author_fields(author_number);
        author_div.append(new_fields);
        load_new_fields(author_div, author_number)

    })
}


function create_author_fields(author_number) {

    if (author_number != 1) {
        return `
        <div class="author" id="author_fields_${author_number}">
            <label>Author Last Name: <input id="author_last_name_${author_number}" name="last_name_${author_number}" type="text" required></label>
            <label>Author First Name: <input id="author_first_name_${author_number}" name="first_name_${author_number}" type="text"></label>
            <label>Author Second Name: <input id="author_second_name_${author_number}" name="second_name_${author_number}" type="text"></label>
            <button id="add_author_button_${author_number}" type="button">Add Author(s)</button>
            <button id="delete_author_button_${author_number}" type="button">Delete Author</button>
        </div>`;
    }
    else {
        return `
        <div class="author" id="author_fields_${author_number}">
            <label>Author Last Name: <input id="author_last_name_${author_number}" name="last_name_${author_number}" type="text" required></label>
            <label>Author First Name: <input id="author_first_name_${author_number}" name="first_name_${author_number}" type="text"></label>
            <label>Author Second Name: <input id="author_second_name_${author_number}" name="second_name_${author_number}" type="text"></label>
            <button id="add_author_button_${author_number}" type="button">Add Author(s)</button>
        </div>`;
    }
}


function count_and_set_authors_number(form) {
    const final_number_of_authors = form.getElementsByClassName('author').length;
    form.querySelector('.final_number_of_authors').value = final_number_of_authors;
    console.log(form.querySelector('.final_number_of_authors').value)
}


function hide_all_forms() {
    let all_forms = document.getElementsByClassName('source_form');
    const number_of_forms = all_forms.length;
    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }
}

