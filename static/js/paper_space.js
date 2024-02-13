document.addEventListener('DOMContentLoaded', function() {

    enable_nav_links();
    enable_rename_form('paper');
    set_disable_scrolling_buttons();
    get_paper_file_info(document.querySelector('#last-file-id').innerHTML);
    // If there are no files?

});

function show_paper_area(area_id) {
    // Hide all areas first then show one
    hide_all_areas('paper');
    const area = document.getElementById(area_id);
    if (!area) {
        return;
    }
    if (area_id === 'actions-area') {
        // Disable scrolling
        disable_scrolling();
    }



    else if (area_id === 'members-area') {
        if (area.getElementsByClassName('member-card').length <= 3) {
            // Disable scrolling if there is no members at workspace
            disable_scrolling();
        }
    }
    else if (area_id === 'papers-area') {
        if (area.getElementsByClassName('paper-card').length <= 4) {
            // Disable scrolling if there is no members at workspace
            disable_scrolling();
        }
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
        // Render last paper file statistics
        document.querySelector('#number_of_words').innerHTML = result.number_of_words;
        document.querySelector('#characters_no_space').innerHTML = result.characters_no_space;
        document.querySelector('#characters_with_space').innerHTML = result.characters_with_space;
    });
}
