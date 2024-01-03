document.addEventListener('DOMContentLoaded', function() {

    const source_id = document.querySelector('#source_id').innerHTML;
    const alter_source_form = document.querySelector('#alter_source_form');
    const add_link_form = document.querySelector('#link_form');
    const new_quote_form = document.querySelector('#new_quote_form');
    const alter_quote_form = document.querySelector('#alter_quote_form');
    const alter_endnote_form = document.querySelector('#alter_endnote_form');
    const delete_quote_buttons = document.getElementsByClassName('delete_quote_buttons');

    alter_source_form.addEventListener('submit', event => {
        event.preventDefault();
        alter_source_info(alter_source_form, source_id);
      });
    
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

    alter_endnote_form.addEventListener('submit', event => {
        event.preventDefault();
        alter_endnote(alter_endnote_form, source_id);
      });

    Array.from(delete_quote_buttons).forEach(button => {
        button.addEventListener('click', () => delete_quote(button.id));
    })
});

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


            // TODO

        }
        else {
            redirect(result.url)
        }
    });
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

function alter_endnote(form, source_id) {

    // Alter-source-endnote view url
    const url = `/alter_source_endnote/${source_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Change space title tag

            console.log(result.endnote);

            // TODO
            
        }
        else {
            redirect(result.url)
        }
    });
}
