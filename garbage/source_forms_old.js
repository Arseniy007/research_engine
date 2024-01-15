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

    const submit_buttons = document.getElementsByClassName('submit_button');
    const number_of_submit_buttons = submit_buttons.length;

    for (let i = 0; i < number_of_submit_buttons; i++) {
        const form_id = submit_buttons[i].parentNode.id;
        submit_buttons[i].addEventListener('click', () => get_lobby_endnotes(form_id));
    }
});

function get_lobby_endnotes(form_id) {

    const url = '/get_lobby_endnotes';
    const form = document.querySelector(`#${form_id}`);
    count_and_set_authors_number(form);

    // Send a POST request to the /get_lobby_endnotes
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        const result_text = `
        APA: ${result.apa_endnote}
        MLA: ${result.mla_endnote}`
        document.querySelector('#result').innerHTML = result_text;
        
    });
}

function show_and_load_form(form_id) {

    // Hide all forms and show the one that user clicked on
    hide_all_forms();
    let form = document.querySelector(`#${form_id}`);
    form.style.display = 'block';

    // Hide this form if button was clicked second time:
    const button_id = form_id.split('_')[0];
    const show_this_form_button = document.querySelector(`#${button_id}`);
    show_this_form_button.addEventListener('click', () => {
        hide_all_forms();
        show_this_form_button.addEventListener('click', () => show_and_load_form(`${button_id}_form`));
    })

    // Set number of authors to 0
    let number_of_authors = 0;
    let number_of_chapter_authors = 0;

    const author_div = form.querySelector('.author_div');
    author_div.innerHTML = create_author_fields(number_of_authors);
    load_new_fields(author_div, number_of_authors);



    
    if (form_id === 'chapter_form') {
       
        // Create separate chapter_author fields for chapter form
        const chapter_author_div = form.querySelector('#chapter_author_div');
        chapter_author_div.innerHTML = create_chapter_author_fields(number_of_chapter_authors);
        load_new_chapter_fields(chapter_author_div, number_of_chapter_authors);
    }
}

function load_new_fields (author_div, author_number) {
    const add_author_button = author_div.querySelector(`#add_author_button_${author_number}`);
    const delete_author_button = author_div.querySelector(`#delete_author_button_${author_number}`);

    if (delete_author_button) {
        delete_author_button.addEventListener('click', function() {
            const author_fields = author_div.querySelector(`#author_fields_${author_number - 1}`);
            author_fields.remove();
            document.querySelector(`#add_author_button_${author_number - 2}`).style.display = 'block';
        })
    }
    author_number++;
    add_author_button.addEventListener('click', function() {
        const new_fields = document.createElement('div');
        new_fields.innerHTML = create_author_fields(author_number);
        author_div.append(new_fields);
        add_author_button.style.display = 'none';
        load_new_fields(author_div, author_number);
    })
}

function load_new_chapter_fields(chapter_author_div, author_number) {
    const add_chapter_author_button = chapter_author_div.querySelector(`#add_chapter_author_button_${author_number}`);
    const delete_chapter_author_button = chapter_author_div.querySelector(`#delete_chapter_author_button_${author_number}`);

    if (delete_chapter_author_button) {
        delete_chapter_author_button.addEventListener('click', function() {
            const chapter_author_fields = chapter_author_div.querySelector(`#chapter_author_fields_${author_number - 1}`);
            chapter_author_fields.remove();
        })
    }
    author_number++;
    add_chapter_author_button.addEventListener('click', function() {
        const new_chapter_fields = document.createElement('div');
        new_chapter_fields.innerHTML = create_chapter_author_fields(author_number);
        chapter_author_div.append(new_chapter_fields);
        load_new_chapter_fields(chapter_author_div, author_number);
    })
}

function count_and_set_authors_number(form) {
    if (form.id === "chapter_form") {
        const final_number_of_chapter_authors = form.getElementsByClassName('chapter_author').length;
        form.querySelector('.final_number_of_chapter_authors').value = final_number_of_chapter_authors;
    }
    const final_number_of_authors = form.getElementsByClassName('author').length;
    form.querySelector('.final_number_of_authors').value = final_number_of_authors;
}


function hide_all_forms() {
    let all_forms = document.getElementsByClassName('source_form');
    const number_of_forms = all_forms.length;
    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }
}

function create_author_fields(author_number) {
    if (author_number != 0) {
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

function create_chapter_author_fields(author_number) {
    if (author_number != 0) {
        return `
        <div class="chapter_author" id="chapter_author_fields_${author_number}">
            <label>Author Last Name: <input id="chapter_author_last_name_${author_number}" name="chapter_last_name_${author_number}" type="text" required></label>
            <label>Author First Name: <input id="chapter_author_first_name_${author_number}" name="chapter_first_name_${author_number}" type="text"></label>
            <label>Author Second Name: <input id="chapter_author_second_name_${author_number}" name="chapter_second_name_${author_number}" type="text"></label>
            <button id="add_chapter_author_button_${author_number}" type="button">Add Chapter Author(s)</button>
            <button id="delete_chapter_author_button_${author_number}" type="button">Delete Author</button>
        </div>`;
    }
    else {
        return `
        <div class="chapter_author" id="chapter_author_fields_${author_number}">
            <label>Author Last Name: <input id="chapter_author_last_name_${author_number}" name="chapter_last_name_${author_number}" type="text" required></label>
            <label>Author First Name: <input id="chapter_author_first_name_${author_number}" name="chapter_first_name_${author_number}" type="text"></label>
            <label>Author Second Name: <input id="chapter_author_second_name_${author_number}" name="chapter_second_name_${author_number}" type="text"></label>
            <button id="add_chapter_author_button_${author_number}" type="button">Add Chapter Author(s)</button>
        </div>`;
    }
}
