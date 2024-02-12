document.addEventListener('DOMContentLoaded', function() {

    enable_nav_links();
    enable_rename_form('paper');
    get_paper_file_info(document.querySelector('#last-file-id').innerHTML);

});

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
