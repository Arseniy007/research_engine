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


async function show_and_load_form(form_id) {

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

    // Load first author field
    const author_div = form.querySelector('.author_div');
    author_div.innerHTML = await render_author_field(number_of_authors);

    // Pre-lode next author field
    load_new_author_field(author_div, number_of_authors);


    //if (form_id === 'chapter_form') {
       
        // Create separate chapter_author fields for chapter form
      //  const chapter_author_div = form.querySelector('#chapter_author_div');
        //chapter_author_div.innerHTML = create_chapter_author_fields(number_of_chapter_authors);
        //load_new_chapter_fields(chapter_author_div, number_of_chapter_authors);
    //}
}



function load_new_author_field (author_div, author_number) {

    // Get adding / deleting buttons
    const add_author_button = author_div.querySelector(`#add-author-button-${author_number}`);
    const delete_author_button = author_div.querySelector(`#delete-author-button-${author_number}`);

    // Set event listener for delete button
    if (delete_author_button) {
        delete_author_button.addEventListener('click', function() {

            // Remove current author field
            author_div.querySelector(`#author-field-${author_number - 1}`).remove();

            // Show both buttons for previous field again
            author_div.querySelector(`#add-author-button-${author_number - 2}`).style.display = 'block';
            const previous_delete_button = author_div.querySelector(`#delete-author-button-${author_number - 2}`);
            if (previous_delete_button) {
                previous_delete_button.style.display = 'block';
            }
        })
    }
    author_number++;

    // Set event listener for add button
    add_author_button.addEventListener('click', async function() {

        // Create new div and render new author field into it
        const new_author_div = document.createElement('div');
        new_author_div.innerHTML = await render_author_field(author_number);
        author_div.append(new_author_div);

        // Hide both delete and add buttons
        add_author_button.style.display = 'none';

        if (delete_author_button) {
            delete_author_button.style.display = 'none';
        }
        // Recursive call
        load_new_author_field(author_div, author_number);
    })
}

async function render_author_field(author_number) {

    // Render-author-fields view url
    const url = `/render_author_field/${author_number}`;

    // Send request to source-space view
    return fetch(url)
    .then(function(response) {
        // When the page is loaded convert it to text
        return response.text()
    })
    .then(function(html) {
        // Initialize the DOM parser
        let parser = new DOMParser();

        // Parse the text
        let author_field_page = parser.parseFromString(html, "text/html");

        // Return author-field-div
        return author_field_page.querySelector('.author-field').innerHTML;
    })
}










function hide_all_forms() {
    let all_forms = document.getElementsByClassName('source_form');
    const number_of_forms = all_forms.length;
    for (let i = 0; i < number_of_forms; i++) {
        all_forms[i].style.display = 'none';
    }
}

function count_and_set_authors_number(form) {
    if (form.id === "chapter_form") {
        const final_number_of_chapter_authors = form.getElementsByClassName('chapter_author').length;
        form.querySelector('.final_number_of_chapter_authors').value = final_number_of_chapter_authors;
    }
    const final_number_of_authors = form.getElementsByClassName('author').length;
    form.querySelector('.final_number_of_authors').value = final_number_of_authors;
}
