document.addEventListener('DOMContentLoaded', function() {

    const source_id = document.querySelector('#source_id').innerHTML;
    const add_link_form = document.querySelector('#link_form');
    const new_quote_form = document.querySelector('#new_quote_form');
    const alter_quote_form = document.querySelector('#alter_quote_form');
    const alter_reference_form = document.querySelector('#alter_reference_form');
    const delete_quote_buttons = document.getElementsByClassName('delete_quote_buttons');
    
    add_link_form.addEventListener('submit', event => {
        event.preventDefault();
        add_link(add_link_form, source_id);
      });

    new_quote_form.addEventListener('submit', event => {
        event.preventDefault();
        add_quote(new_quote_form, source_id);
      });

    alter_quote_form.addEventListener('submit', event => {
        event.preventDefault();
        alter_quote(alter_quote_form, source_id);
      });

    alter_reference_form.addEventListener('submit', event => {
        event.preventDefault();
        alter_reference(alter_reference_form, source_id);
      });

    Array.from(delete_quote_buttons).forEach(button => {
        button.addEventListener('click', () => delete_quote(button.id));
    })
});

function show_or_hide_source_settings() {

    const source_div = document.querySelector('#source-space');
    const source_settings_div = document.querySelector('#source-settings');

    if (source_settings_div.style.display === 'none') {
        source_div.style.display = 'none';
        source_settings_div.style.display = 'block';
    }
    else {
        source_settings_div.style.display = 'none';
        source_div.style.display = 'block';
    }
}

function alter_source_info(form, source_id) {

    // Alter-source-info view url
    const url = `/alter_source_info/${source_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {

            // updated source space
            load_and_show_source_space(source_id)
        }
        else {
            redirect(result.url)
        }
    });
}

function load_and_show_source_space(source_id) {

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
        source_space_div.innerHTML = source_space_page.querySelector('#source-space-div').innerHTML;
    })
}


function add_link(form, source_id) {

    // Add-link-to-source view url
    const url = `/add_link_to_source/${source_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
  
            // TODO

            let link_div = document.querySelector('#source_link');
            link_div.querySelector('#link_tag').href = result.link;
            link_div.style.display = 'block';
        }
        else {
            redirect(result.url)
        }
    });
}

function add_quote(form, source_id) {

    // Add-quote view url
    const url = `/add_quote/${source_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {

            console.log(result.quote)

            // TODO
            
        }
        else {
            redirect(result.url)
        }
    });
}

function delete_quote(quote_id) {

    // Delete-quote view url
    const url = `/delete_quote/${quote_id}`;

    // Send GET request
    fetch(url)
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Remove quote div from page
            document.querySelector(`#quote_${quote_id}`).remove()

            // TODO Animation!
            
        }
        // TODO
    });
}

function alter_quote(form, quote_id) {

    // Alter-quote view url
    const url = `/alter_quote/${quote_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Change space title tag

            console.log(result.altered_quote);

            // TODO
            
        }
        else {
            redirect(result.url)
        }
    });
}

function alter_reference(form, source_id) {

    // Alter-source-endnote view url
    const url = `/alter_source_reference/${source_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Change space title tag

            console.log(result.reference);

            // TODO
            
        }
        else {
            redirect(result.url)
        }
    });
}
