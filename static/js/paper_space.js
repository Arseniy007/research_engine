document.addEventListener('DOMContentLoaded', function() {

    const settings_form = document.querySelector('#settings-form');
    settings_form.addEventListener('submit', event => {
        if (!settings_form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        settings_form.classList.add('was-validated');
    })

    get_paper_file_info(document.querySelector('#last_file_id').innerHTML);


});


function get_paper_file_info(file_id) {

    // Paper info API route
    const url = `/paper_file_info/${file_id}`;

    // Send request
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        
        document.querySelector('#number_of_words').innerHTML = result.number_of_words;


    });





}




function handleErrors(response, url) {
    if (!response.ok) {
        redirect(url)
    }
    return response;
}




function rename_paper(form, paper_id) {

    // Rename-paper url
    const url = `/rename_paper/${paper_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Change space title tag
            document.querySelector('#paper_title').innerHTML = result.new_title;
        }
        else {
            redirect(result.url)
        }
    });
}
