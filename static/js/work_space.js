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

        // Get empty divs for pasting
        let source_space_div = document.querySelector(`#source-space-div-${source_id}`);
        let source_footer_div = document.querySelector(`#source-footer-div-${source_id}`);

        // Past source space header
        let source_space_header = source_space_page.querySelector('#source-space-header');
        document.querySelector(`#source-space-label-${source_id}`).innerHTML = source_space_header.innerHTML;

        // Past source space body and footer
        source_space_div.innerHTML = source_space_page.querySelector('#source-space-div').innerHTML;
        source_footer_div.innerHTML= source_space_page.querySelector('#source-footer').innerHTML;
  
        const edit_forms = document.getElementsByClassName('edit-form');
        Array.from(edit_forms).forEach(form => {
            form.addEventListener('change', function() {
                form.classList.add('was-changed')
            })
        })

        // Get open-source-file-button to display file
        const source_file_id = source_space_div.querySelector('#source-file-id').innerHTML;
        const open_file_button = document.querySelector(`#open-source-file-button-${source_id}`);
        if (open_file_button) {
            open_file_button.href = `/source_file/${source_file_id}`;
        }
    })
}

async function submit_source_forms(source_id) {

    // TODO
    // how to update source button at modal footer?????????????

    // Get all changed forms
    const forms = document.getElementsByClassName('was-changed');

    if (!forms.length) {
        // In case no form was changed
        return;
    }

    for await (const form of forms) {
        if (form.id === `alter-source-form-${source_id }`) {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source main info
                await alter_source_info(form, source_id);
            }
        }
        else if (form.id === `add-link-form-${source_id}`) {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source link
                await add_link_to_source(form, source_id);
            }
        }
        else if (form.id === `upload-file-form-${source_id}`) {
            // Save new source file
            await upload_source_file(form, source_id);
        }
    }
    // Update source space
    load_and_show_source_space(source_id);
}

async function alter_source_info(form, source_id) {

    // Alter-source-info view url
    const url = `/alter_source_info/${source_id}`;

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
    
        }
        else {
            return redirect(result.url)
        }
    })
}

async function add_link_to_source(form, source_id) {

    // Add-link-to-source view url
    const url = `/add_link_to_source/${source_id}`;

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return redirect(result.url)
        }
    });
}

async function upload_source_file(form, source_id) {

    // Add-link-to-source view url
    const url = `/upload_source_file/${source_id}`;

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return redirect(result.url)
        }
    });
}

function show_or_hide_source_settings(source_id) {

    const source_div = document.querySelector('#source-space');
    const source_settings_div = document.querySelector('#source-settings');

    // Get all buttons
    const show_settings_button = document.querySelector(`#show-source-settings-button-${source_id}`);
    const close_settings_button = document.querySelector(`#close-source-settings-button-${source_id}`);
    const link_button = document.querySelector(`#source-link-button-${source_id}`);
    const open_file_button = document.querySelector(`#open-source-file-button-${source_id}`);
    const arrow_buttons = document.getElementsByClassName('arrow-button');

    if (source_settings_div.style.display === 'none') {
        source_div.style.display = 'none';
        source_settings_div.style.display = 'block';

        // Change all buttons
        show_settings_button.style.display = 'none';
        close_settings_button.style.display = 'inline-block';

        if (open_file_button) {
            open_file_button.style.display = 'none';
        }

        if (link_button) {
            link_button.style.display = 'none';
        }

        Array.from(arrow_buttons).forEach(button => {
            button.style.display = 'none';
        })
        
    }
    else {
        source_settings_div.style.display = 'none';
        source_div.style.display = 'block';

        // Change all buttons
        close_settings_button.style.display = 'none';
        show_settings_button.style.display = 'inline-block';

        if (open_file_button) {
            open_file_button.style.display = 'inline-block';
        }

        if (link_button) {
            link_button.style.display = 'inline-block';
        }

        Array.from(arrow_buttons).forEach(button => {
            button.style.display = 'inline-block';
        })
    }
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
