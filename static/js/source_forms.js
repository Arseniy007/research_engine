document.addEventListener('DOMContentLoaded', function() {
    
    const show_form_buttons = document.getElementsByClassName('show_form_button');
    Array.from(show_form_buttons).forEach(button => {
        button.addEventListener('click', () => show_and_load_form(`${button.id}_form`));
    })

    const forms = document.getElementsByClassName('source_form');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', () => count_and_set_authors_number(form));
    })

    const submit_buttons = document.getElementsByClassName('submit_button');
    Array.from(submit_buttons).forEach(button => {
        button.addEventListener('click', () => get_lobby_endnotes(button.parentNode.id))
    })
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
    const author_div = form.querySelector('.author-div');
    console.log(author_div);
    author_div.innerHTML = await render_author_field(number_of_authors);

    // Pre-lode next author field
    load_new_author_field(author_div, number_of_authors);

    if (form_id === 'chapter_form') {
        // Load first chapter-author field
        const chapter_author_div = form.querySelector('#chapter-author-div');
        chapter_author_div.innerHTML = await render_author_field(number_of_chapter_authors, chapter=true);

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
            author_div.querySelector(`#${chapter}add-author-button-${author_number - 2}`).style.display = 'block';
            const previous_delete_button = author_div.querySelector(`#${chapter}delete-author-button-${author_number - 2}`);
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
        new_author_div.innerHTML = await render_author_field(author_number, chapter);
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
    let url = '';
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
        let author_field_page = parser.parseFromString(html, "text/html");

        // Return author-field-div
        return author_field_page.querySelector('.author-field').innerHTML;
    })
}

function hide_all_forms() {
    const all_forms = document.getElementsByClassName('source_form');
    Array.from(all_forms).forEach(form => {
        form.style.display = 'none';
    })
}

function count_and_set_authors_number(form) {

    if (form.id === "chapter_form") {
        // Count how many "chapter-author" divs are there
        form.querySelector('.final_number_of_chapter_authors').value = form.getElementsByClassName('chapter-author').length;
    }
    // Count how many "author" divs are there
    form.querySelector('.final_number_of_authors').value = form.getElementsByClassName('author').length;
}

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
        // TODO
        const result_text = `
        APA: ${result.apa_endnote}
        MLA: ${result.mla_endnote}`
        document.querySelector('#result').innerHTML = result_text;
        
    });
}
