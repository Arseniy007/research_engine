document.addEventListener('DOMContentLoaded', function() {

    // Render paper file related info
    get_paper_file_info(document.querySelector('#last-file-id').innerHTML);

    // Show and hide rename paper form
    const header = document.querySelector('#header');
    const header_text = document.querySelector('#header-text');
    const edit_symbol = document.querySelector('#edit-title-symbol');

    header.addEventListener('mouseenter', () => {
        edit_symbol.addEventListener('click', () => {
            header_text.innerHTML = document.querySelector('#rename-paper-form-div').innerHTML;
        });
        edit_symbol.style.display = 'inline-block';
    });
    header.addEventListener('mouseleave', () => edit_symbol.style.display = 'none');
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
