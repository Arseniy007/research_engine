document.addEventListener('DOMContentLoaded', function() {

    const space_id = document.querySelector('#space_id').innerHTML;
    const rename_form = document.querySelector('#rename_form');

    rename_form.addEventListener('submit', event => {
        event.preventDefault();
        rename_space(rename_form, space_id);
      });

});

function show_source_space(source_id) {

    // Source-space view url
    const url = `/source_space/${source_id}`;

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
        let source_space_page = parser.parseFromString(html, "text/html");

        // Get empty div for pasting
        let source_space_div = document.querySelector(`#source-space-div-${source_id}`);

        // Past fetched html
        source_space_div.innerHTML = source_space_page.querySelector('#source_space').innerHTML;
    })
}

function show_paper_space(paper_id) {

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
        let paper_space_div = document.querySelector(`#paper-space-div-${paper_id}`);

        // Past fetched html
        paper_space_div.innerHTML = paper_space_page.querySelector('#paper_space').innerHTML;
    })
}










function rename_space(form, space_id) {

    // Rename-space view url
    const url = `/rename_space/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Change space title tag
            document.querySelector('#space_title').innerHTML = result.new_title;
        }
        else {
            redirect(result.url)
        }
    });
}


function redirect(url) {
    // Imitate django redirect func
    window.location.replace(url)
}


function handleErrors(response, url) {
    if (!response.ok) {
        if (response.statusText === 'Forbidden') {
            redirect(url)
        }

        // TODO: other errors 
    }
    return response;
}