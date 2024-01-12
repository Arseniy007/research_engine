document.addEventListener('DOMContentLoaded', function() {

    const space_id = document.querySelector('#space_id').innerHTML;
    const rename_space_form = document.querySelector('#rename_space_form');
    const link_form = document.querySelector('#link_form');

    rename_space_form.addEventListener('submit', event => {
        event.preventDefault();
        rename_space(rename_space_form, space_id);
      });

    link_form.addEventListener('submit', event => {
        event.preventDefault();
        add_link(link_form, space_id);
      });


});

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

        // Past source space header
        document.querySelector(`#source-space-label-${source_id}`).innerHTML = source_space_page.querySelector('#source-space-header').innerHTML;

        // Past source space body
        source_space_div.innerHTML = source_space_page.querySelector('#source-space-div').innerHTML;

        set_form_validation();

        // Get all new forms
        const alter_source_form = document.querySelector('#alter-source-form');
        const alter_source_reference_form = document.querySelector('#alter-reference-form');

        alter_source_form.addEventListener('submit', event => {

            // Set form validation
            if (!alter_source_form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
                alter_source_form.classList.add('was-validated')
            }
            else {
                event.preventDefault();
                alter_source_info(alter_source_form, source_id);
            }
          });

        alter_source_reference_form.addEventListener('submit', event => {

            // Set form validation
            if (!alter_source_reference_form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
                alter_source_reference_form.classList.add('was-validated')
            }
            else {
                event.preventDefault();
                alter_source_reference(alter_source_reference_form, source_id);
            }
        });

        // Get open-source-file button to display file
        const source_file_id = source_space_div.querySelector('#source-file-id').innerHTML;
        document.querySelector(`#open-source-file-button-${source_id}`).href = `/source_file/${source_file_id}`;
    })
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

            // Updated source space
            load_and_show_source_space(source_id)
        }
        else {
            redirect(result.url)
        }
    });
}

function alter_source_reference(form, source_id) {

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

            // Updated source space
            load_and_show_source_space(source_id)
        }
        else {
            redirect(result.url)
        }
    });
}

function show_or_hide_source_settings(source_id) {

    const source_div = document.querySelector('#source-space');
    const source_settings_div = document.querySelector('#source-settings');

    // Get all buttons
    const show_settings_button = document.querySelector(`#show-source-settings-button-${source_id}`);
    const close_settings_button = document.querySelector(`#close-source-settings-button-${source_id}`);
    const close_button = document.querySelector(`#close-source-button-${source_id}`);
    const link_button = document.querySelector(`#source-link-button-${source_id}`);
    const open_file_button = document.querySelector(`#open-source-file-button-${source_id}`);

    if (source_settings_div.style.display === 'none') {
        source_div.style.display = 'none';
        source_settings_div.style.display = 'block';

        // Change all buttons
        close_button.style.display = 'none';
        show_settings_button.style.display = 'none';
        close_settings_button.style.display = 'block';

        if (open_file_button) {
            open_file_button.style.display = 'none';
        }

        if (link_button) {
            link_button.style.display = 'none';
        }
        
    }
    else {
        source_settings_div.style.display = 'none';
        source_div.style.display = 'block';

        // Change all buttons
        close_settings_button.style.display = 'none';
        show_settings_button.style.display = 'inline';
        close_button.style.display = 'block';

        if (open_file_button) {
            open_file_button.style.display = 'inline';
        }

        if (link_button) {
            link_button.style.display = 'inline';
        }
    }
}

function open_source_file(source_file_id) {

    // Display source-file url
    const url = `/source_file/${source_file_id}`;





}



function rename_space(form, space_id) {

    // Rename-space url
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

function add_link(form, space_id) {

    // Add-link view url
    const url = `/add_link_to_space/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            
            console.log(result.link_name);
            // TODO!
            // What to do?
        }
        else {
            redirect(result.url)
        }
    });
}

function alter_link(link_id) {

    // Alter-link view url
    const url = `/alter_link/${link_id}`;

    // TODO

}

function delete_link(link_id) {

    // Delete-link view url
    const url = `/delete_link/${link_id}`;

    // Send request to delete_link view
    fetch(url)
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            
            document.querySelector(`#link_${link_id}`).remove();
        }
        else {
            console.log("error")
        }
    });
    // TODO: animation!
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
