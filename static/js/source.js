document.addEventListener('DOMContentLoaded', function() {

    const source_id = document.querySelector('#source_id').innerHTML;
    const add_link_form = document.querySelector('#link-form');
    const new_quote_form = document.querySelector('#new_quote_form');
    const alter_quote_form = document.querySelector('#alter_quote_form');
    const delete_quote_buttons = document.getElementsByClassName('delete_quote_buttons');
    
    add_link_form.addEventListener('submit', event => {
        event.preventDefault();
        add_link_to_source(add_link_form, source_id);
      });

    new_quote_form.addEventListener('submit', event => {
        event.preventDefault();
        add_quote(new_quote_form, source_id);
      });

    alter_quote_form.addEventListener('submit', event => {
        event.preventDefault();
        alter_quote(alter_quote_form, source_id);
      });

    Array.from(delete_quote_buttons).forEach(button => {
        button.addEventListener('click', () => delete_quote(button.id));
    })
});


function delete_source_link(source_id) {

    // Delete-source-link view url
    const url = `/delete_source_link/${source_id}`;

    // Send GET request
    fetch(url)
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // TODO            
        }
        // TODO
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

