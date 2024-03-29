function hide_all_forms() {
    const all_forms = document.getElementsByClassName('source-form-area');
    Array.from(all_forms).forEach(form => {
        form.style.display = 'none';
    })

    // Hide result if shown
    const reference_result = document.getElementById('reference-result');
    if (reference_result) {
        reference_result.style.display = 'none';
    }
}

function show_source_creation_form() {
    // When source type gets selected - show selected form
    const source_type_selector = document.getElementById('source-type-selector');
    source_type_selector.addEventListener('change', () => {
        const selected_source_type = source_type_selector.value;
        if (selected_source_type) {
            load_source_form(selected_source_type);
        }
        else {
            hide_all_forms();
        }
    });
}

async function load_source_form(form_id) {

    // Hide all forms and show the one that user clicked on
    hide_all_forms();
    const form = document.getElementById(form_id);

    if (document.getElementById('reference-result')) {
        // For lobby page
        document.getElementById('reference-result').style.display = 'none';
        form.querySelector('.get-reference-button').style.display = 'block';
        form.querySelector('.source-form').reset();
    }

    form.style.display = 'block';

    // Set number of authors to 0
    let number_of_authors = 0;
    let number_of_chapter_authors = 0;

    // Load first author field
    const author_div = form.querySelector('.author-div');
    const author_form_body = await render_author_field(number_of_authors);
    author_div.innerHTML = author_form_body.innerHTML;
    author_div.id = author_form_body.id
    author_div.className = 'author';

    // Pre-lode next author field
    load_new_author_field(author_div, number_of_authors);

    if (form_id === 'chapter-form') {
        // Load first chapter-author field
        const chapter_author_div = form.querySelector('#chapter-author-div');
        const chapter_author_form_body = await render_author_field(number_of_chapter_authors, chapter=true);
        chapter_author_div.innerHTML = chapter_author_form_body.innerHTML;
        chapter_author_div.id = chapter_author_form_body.id
        chapter_author_div.className = 'chapter-author';

        // Pre-lode next chapter-author field
        load_new_author_field(chapter_author_div, number_of_chapter_authors, is_chapter=true);
    }
}

function load_new_author_field (author_div, author_number, is_chapter=false) {

    // If we are dealing with chapter author - prefix ids / classes with "chapter-"
    let chapter = '';
    if (is_chapter) {
        chapter = 'chapter-'
    }

    // Get adding / deleting buttons
    const add_author_button = author_div.querySelector(`#${chapter}add-author-button-${author_number}`);
    const delete_author_button = author_div.querySelector(`#${chapter}delete-author-button-${author_number}`);

    // Set event listener for delete button
    if (delete_author_button) {
        delete_author_button.addEventListener('click', function() {

            // Remove current author field
            author_div.querySelector(`#${chapter}author-field-${author_number - 1}`).remove();

            // Show both buttons for previous field again
            author_div.querySelector(`#${chapter}add-author-button-${author_number - 2}`).style.display = 'inline-block';
            const previous_delete_button = author_div.querySelector(`#${chapter}delete-author-button-${author_number - 2}`);
            if (previous_delete_button) {
                previous_delete_button.style.display = 'inline-block';
            }
        })
    }
    author_number++;

    // Set event listener for add button
    add_author_button.addEventListener('click', async function() {

        // Create new div and render new author field into it
        const new_author_div = document.createElement('div');
        const author_form_body = await render_author_field(author_number, chapter);
        new_author_div.innerHTML = author_form_body.innerHTML;
        new_author_div.id = author_form_body.id
        new_author_div.className = `${chapter}author`;

        //new_author_div.innerHTML = await render_author_field(author_number, chapter);
        author_div.append(new_author_div);

        // Hide both delete and add buttons
        add_author_button.style.display = 'none';
        if (delete_author_button) {
            delete_author_button.style.display = 'none';
        }
        // Recursive call
        load_new_author_field(author_div, author_number, chapter);
    })
}

async function render_author_field(author_number, chapter=false) {

    // Render-author-fields view url
    let url;
    if (chapter) {
        url = `/render_author_field/${author_number}/1`;
    }
    else {
        url = `/render_author_field/${author_number}/0`;
    }

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
        const author_field_page = parser.parseFromString(html, "text/html");

        // Return author-field-div
        return author_field_page.querySelector('.form-body');
    })
}

function count_and_set_authors_number(form) {

    if (form.parentNode.id === "chapter-form") {
        // Count how many "chapter-author" divs are there
        form.querySelector('.final_number_of_chapter_authors').value = form.getElementsByClassName('chapter-author').length;
    }
    // Count how many "author" divs are there
    form.querySelector('.final_number_of_authors').value = form.getElementsByClassName('author').length;
}

function set_source_creation_forms_validation(space_id) {
    // Get all forms
    const forms = document.getElementsByClassName('source-form');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            // Set form Validation
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated')
              }
            else {
                // If everything alright - submit form with custom function
                event.preventDefault();
                count_and_set_authors_number(form);
                submit_source_form(form, space_id);
            }
        }, false)
    })
}

function submit_source_form(form, space_id) {
    // Add-source API route
    const url = `/add_source/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        // Redirect to new source space or back in case of error
        window.location.replace(result.url)
    });
}

function set_reference_forms_submission() {
    const get_reference_buttons = document.getElementsByClassName('get-reference-button');
    Array.from(get_reference_buttons).forEach(button => {
        button.addEventListener('click', () => get_quick_reference(button.parentNode.parentNode.parentNode.id));
    })
}

function get_quick_reference(form_id) {

    const url = '/get_quick_reference';
    const form = document.getElementById(form_id).querySelector('.source-form');
    const error_message = document.querySelector('.form-error-message');

    // Set form validation
    if (!form.checkValidity()) {
        form.classList.add('was-validated')
        return;
    }

    count_and_set_authors_number(form);

    // Send a POST request to the /get_lobby_endnotes
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Hide error message in case it's shown
            if (error_message.style.display == 'block') {
                error_message.style.display = 'none';
            }
            // Hide get reference button and submitted form
            form.querySelector('.get-reference-button').style.display = 'none';
            hide_all_forms();

            // Show fields
            document.getElementById('reference-result').style.display = 'block';

            // Get result fields
            const apa_field = document.getElementById('reference-result-field-apa');
            const mla_field = document.getElementById('reference-result-field-mla');

            // Paste result references and auto grow textareas
            apa_field.value = result.reference.apa_endnote;
            mla_field.value = result.reference.mla_endnote;
            adjust_textarea_height(apa_field);
            adjust_textarea_height(mla_field);
        }
        else {
            // Error case
            error_message.style.display = 'block';
        }
    });
}

function copy_reference(style) {
    const textarea = document.getElementById(`reference-result-field-${style}`);
    if (!textarea) {
        return;
    }
    textarea.select();
    document.execCommand("copy");
}
