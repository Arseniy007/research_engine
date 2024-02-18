document.addEventListener('DOMContentLoaded', function() {

    enable_nav_links();
    enable_rename_form('paper');
    set_enable_scrolling_buttons();
    set_disable_scrolling_buttons();




});

function show_paper_area(area_id) {
    // Hide all areas first then show one
    hide_all_areas('paper');
    const area = document.getElementById(area_id);
    if (!area) {
        return;
    }
    if (area_id === 'main-area') {
        // Disable scrolling if no bibliography
        if (!area.querySelector('#bibliography-textarea')) {
            disable_scrolling();           
        }
    }
    else if (area_id === 'sources-area') {
        // Disable scrolling if there is no form
        if (!area.querySelector('#choose-sources-button')) {
            disable_scrolling();
        }
        // Disable scrolling if there is less than 8 sources
        else if (area.getElementsByClassName('source-card').length < 5) {
            disable_scrolling();
        }
        // Hide info message
        if (document.getElementsByClassName('messages').length > 0) {
            Array.from(document.getElementsByClassName('messages')).forEach(message => {message.style.display = 'none'});
        }
    }
    else if (area_id === 'files-area') {
        // Disable scrolling if there is no file history
        if (!area.querySelector('#file-history')) {
            disable_scrolling();
        }
    }
    else if (area_id === 'actions-area') {
        // Disable scrolling
        disable_scrolling();
    }
    area.style.display = '';
}

function get_paper_file_info(file_id) {

    // Paper info API route
    const url = `/paper_file_info/${file_id}`;

    // Send request
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {

        // Error case
        //TODO

        // Render last paper file statistics
        document.getElementById('number-of-words').innerHTML = result.number_of_words;
        document.getElementById('characters-no-space').innerHTML = result.characters_no_space;
        document.getElementById('characters-with-space').innerHTML = result.characters_with_space;
        document.getElementById('number-of-pages').innerHTML = result.number_of_pages;
    });
}

function copy_bibliography() {
    const textarea = document.getElementById('bibliography-textarea')
    if (!textarea) {
        return;
    }
    textarea.select();
    document.execCommand("copy");
}

function mark_source_as_checked(source_id) {
    // Get right card
    const source_card = document.getElementById(`source-card-${source_id}`);

    // Check or uncheck source checkbox
    const check_box = source_card.querySelector(`#source-checkbox-${source_id}`);
    if (check_box.checked === false) {
        check_box.checked = true;
    }
    else {
        check_box.checked = false;
    }
}

function submit_choose_source_form(paper_id) {

    // Select sources API route
    const url = `/select_sources/${paper_id}`;
    const form = document.getElementById('choose-source-form');

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Reload page
            return redirect(result.url);
        }
    });
}
