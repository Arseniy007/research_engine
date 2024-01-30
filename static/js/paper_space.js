document.addEventListener('DOMContentLoaded', function() {

    const settings_form = document.querySelector('#settings-form');
    settings_form.addEventListener('submit', event => {
        if (!settings_form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        settings_form.classList.add('was-validated');
    })

});

function load_and_show_paper_space(paper_id) {

    // TODO
    // Delete???

    // Source-space view url
    const url = `/paper_space/${paper_id}`;

    // Send request to source-space view
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(function(response) {
        // When the page is loaded convert it to text
        return response.text()
    })
    .then(function(html) {
        // Initialize the DOM parser
        let parser = new DOMParser();

        // Parse the text
        let paper_space_page = parser.parseFromString(html, "text/html");

        // Get empty div for pasting
        const paper_space_div = document.querySelector(`#paper-space-div-${paper_id}`);

        // Past fetched html
        paper_space_div.innerHTML = paper_space_page.querySelector('#paper_space').innerHTML;

        const rename_paper_form = paper_space_div.querySelector('#rename_paper_form');
    
        rename_paper_form.addEventListener('submit', event => {
            event.preventDefault();
            rename_paper(rename_paper_form, paper_id);
          });
    })
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
