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
        if (!area.querySelector('#choose-sources')) {
            disable_scrolling();
        }
        // Disable scrolling if there is less than 8 sources
        else if (area.getElementsByClassName('source-card').length < 9) {
            disable_scrolling();
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
