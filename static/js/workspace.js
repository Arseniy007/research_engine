document.addEventListener('DOMContentLoaded', function() {
    enable_nav_links();
    enable_rename_form('workspace');
    set_enable_scrolling_buttons();
    set_disable_scrolling_buttons();
});

function show_workspace_area(area_id) {
    // Hide all areas first then show one
    hide_all_areas('workspace');
    const area = document.getElementById(area_id);
    if (!area) {
        return;
    }
    if (area_id === 'sources-area') {
        if (area.getElementsByClassName('source-card').length < 4) {
            // Disable scrolling if there is less than 8 sources
            disable_scrolling();
        }
    }
    else if (area_id === 'members-area') {
        if (area.getElementsByClassName('member-card').length <= 3) {
            // Disable scrolling if there is no members at workspace
            disable_scrolling();
        }
    }
    else if (area_id === 'papers-area') {
        if (area.getElementsByClassName('paper-card').length <= 4) {
            // Disable scrolling if there is no members at workspace
            disable_scrolling();
        }
    }
    else if (area_id === 'actions-area') {
        // Disable scrolling
        disable_scrolling();
    }
    area.style.display = '';
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
        const source_space_page = parser.parseFromString(html, "text/html");

        // Get empty div for pasting
        const source_space_div = document.querySelector(`#source-space-div-${source_id}`);

        // Past source space header
        const source_space_header = source_space_page.querySelector('#source-space-header');
        document.querySelector(`#source-space-label-${source_id}`).innerHTML = source_space_header.innerHTML;

        // Past source space body
        source_space_div.innerHTML = source_space_page.querySelector('#source-space-div').innerHTML;
        
        // Set validation for source-edit-forms
        const edit_forms = document.getElementsByClassName('edit-form');
        Array.from(edit_forms).forEach(form => {
            form.addEventListener('change', function() {
                form.classList.add('was-changed')
            })
        })
    })
}

async function show_new_paper_form(space_id) {
    // Open sidenav 
    const nav = document.querySelector(".sidenav");
    nav.style.width = "100%";
    nav.style.textAlign = 'center';
    nav.style.background = GRAY;
    nav.classList.add('z-index-max');
    nav.querySelector('#sidenav-closed-view').style.display = 'none';
    nav.querySelector('#re-main-button').style.marginRight = '15px';

    // Load content
    nav.querySelector('#index-container').innerHTML = document.querySelector('#new-paper-form').innerHTML;

    // Set form validation
    set_index_form_validation(nav);

    // Show everything
    nav.querySelector('#sidenav-full-view').style.display = 'block';

    // Set form validation
    const paper_form = nav.querySelector('#paper-form');
    paper_form.addEventListener('submit', event => {
        if (!paper_form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            paper_form.classList.add('was-validated');
        }
        else {
            event.preventDefault();
            create_new_paper(paper_form, space_id);
        }
    })

    // Pause for less than 1 sec and then show form
    await delay(800);
    nav.querySelector('#open-new-paper-form').click();
}

function create_new_paper(form, space_id) {

    // Create-paper route
    const url = `/create_paper/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Redirect to new workspace
            window.location.replace(result.url);
        }
        else {
            // Show error message
            document.querySelector('#index-error-message').style.display = 'block';
        }
    });
}

function invite_to_work_space(space_id) {

    // Invitation API route
    const url = `/invite_to_space/${space_id}`;

    // Send request
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        // Render results inside opened modal
        document.querySelector('#invitation-code-textarea').innerHTML = result.invitation_code;
        document.querySelector('#invitation-link-textarea').innerHTML = result.invitation_link;
        enable_scrolling();
    });
}

function share_space_sources(space_id) {

    // Invitation API route
    const url = `/share_sources/${space_id}`;

    // Send request
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        // Render results inside opened modal
        document.querySelector('#sources-code-textarea').innerHTML = result.sources_code;
        document.querySelector('#sources-link-textarea').innerHTML = result.sources_link;
        enable_scrolling();
    });
}

function copy_invitation(kind, type) {
    const textarea = document.querySelector(`#${kind}-${type}-textarea`);
    if (!textarea) {
        return;
    }
    textarea.select();
    document.execCommand("copy");
}
