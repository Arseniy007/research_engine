const GRAY = '#222222';
const NORMAL = '#0b121b';

document.addEventListener('DOMContentLoaded', () => {
    // Enable popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
});

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function disable_scrolling() {
    document.getElementById('content').classList.add('stop-scrolling');
}

function enable_scrolling() {
    document.getElementById('content').classList.remove('stop-scrolling');
}

function dropdown_spaces() {
    document.getElementById("spaces-dropdown").classList.toggle("show");
}

function dropdown_papers() {
    document.getElementById("papers-dropdown").classList.toggle("show");
}

function delay(milliseconds){
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}

function handleErrors(response, url) {
    if (!response.ok) {
        redirect(url)
    }
    return response;
}

function redirect(url) {
    // Imitate django redirect func
    window.location.replace(url)
}

async function openNav() {
    // Open sidenav (make it full width)
    const nav = document.querySelector(".sidenav");
    nav.style.width = "100%";
    nav.style.textAlign = 'center';
    nav.style.background = GRAY;
    nav.classList.add('z-index-max');
    nav.querySelector('#sidenav-closed-view').style.display = 'none';
    nav.querySelector('#re-main-button').style.marginRight = '15px';

    // Load content
    const index_content = await load_index_data();
    nav.querySelector('#index-container').innerHTML = index_content.innerHTML;

    // Set form validation
    set_index_form_validation(nav);

    // Show everything
    nav.querySelector('#sidenav-full-view').style.display = 'block';
}

async function closeNav() {
    // Return sidenav to its side
    const nav = document.querySelector(".sidenav");
    nav.style.width = "270px";
    nav.style.textAlign = 'left';
    nav.style.background = NORMAL;
    nav.querySelector('#re-main-button').style.marginRight = '30px';
    nav.querySelector('#sidenav-full-view').style.display = 'none';
    nav.querySelector('#sidenav-closed-view').style.display = 'block';
    await delay(500);
    nav.classList.remove('z-index-max');
}

async function load_index_data() {
    // API route for loading index content
    const url = '/index_content';

    // Send request
    return fetch(url)
    .then(function(response) {
        // When the page is loaded convert it to text
        return response.text()
    })
    .then(function(html) {
        // Initialize the DOM parser
        let parser = new DOMParser();

        // Parse the text
        const index_page = parser.parseFromString(html, "text/html");

        // Return content
        return index_page.querySelector('#index-div');
    })
}

function set_index_form_validation(nav) {
    // Get all index-forms
    const index_forms = nav.getElementsByClassName('index-form');

    Array.from(index_forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
            }
            else {
                if (form.id === 'create-space-form') {
                    event.preventDefault();
                    create_new_work_space(form);
                }
                else if (form.id === 'receive-invitation-form') {
                    event.preventDefault();
                    receive_invitation(form);
                }
                else if (form.id === 'shared-sources-form') {
                    event.preventDefault();
                    receive_shared_sources(form);
                }
                else {
                    // Error case
                    document.getElementById('index-error-message').style.display = 'block';
                }
            }
        })
    })
}

function create_new_work_space(form) {
    // Create-workspace route
    const url = '/create_work_space';

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
            document.getElementById('index-error-message').style.display = 'block';
        }
    });
}

function receive_invitation(form) {
    // API route
    const url = '/receive_invitation';

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
            const invitation_error_message = document.getElementById('invitation-error-message');
            let error_message;
            if (invitation_error_message) {
                error_message = invitation_error_message;
                document.getElementById('invitation-div').style.display = 'none';
            }
            else {
                error_message = document.getElementById('index-error-message');
            }
            error_message.querySelector('.error').innerHTML = `<a href="${result.url}" style="color: black">${result.message}</a>`;
            error_message.style.display = 'block';
        }
    });
}

function receive_shared_sources(form) {
    // API route
    const url = '/receive_shared_sources';

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Redirect to new workspace / download url
            window.location.replace(result.url);
        }
        else {
            // Show error message
            const invitation_error_message = document.getElementById('invitation-error-message');
            let error_message;
            if (invitation_error_message) {
                error_message = invitation_error_message;
                document.getElementById('sources-div').style.display = 'none';
            }
            else {
                error_message = document.getElementById('index-error-message');
            }
            error_message.querySelector('.error').innerHTML = `<a href="${result.url}" style="color: black">${result.message}</a>`;
            error_message.style.display = 'block';
        }
    });
}

function search_source() {
    // Get all sources
    const sources = document.getElementsByClassName("source-card");
    const titles = document.getElementsByClassName("source-title");
    const authors = document.getElementsByClassName("source-author");
    const number_of_sources = sources.length;

    // Get input
    let input = document.getElementById("search-box");
    input = input.value.toLowerCase();

    // Loop through all sources, and hide those who don't match the search query
    for (let i = 0; i < number_of_sources; i++) {
        if (!titles[i].innerHTML.toLowerCase().includes(input) && !authors[i].innerHTML.toLowerCase().includes(input)) {

            sources[i].style.display = 'none';
        }
        else {
            sources[i].style.display = '';
        }
    }
}

function set_form_validation() {
    // Fetch all the forms
    const forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated')
      }, false)
    })
}

function hide_all_areas(page) {
    // Hide all parts of workspace / paper pages
    const areas = document.getElementsByClassName(`${page}-area`);
    Array.from(areas).forEach(array => {array.style.display = 'none'})

    enable_scrolling();
}

function enable_nav_links() {
    // For workspace and paper pages
    const navTabs = document.querySelectorAll("#nav-tabs > a");
    navTabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            navTabs.forEach((tab) => {
                tab.classList.remove("active");
            });
            tab.classList.add("active");
        });
    });
}

function enable_rename_form(page) {
    // Show and hide rename space / paper forms
    const header = document.getElementById('header');
    const header_text = document.getElementById('header-text');
    const edit_symbol = document.getElementById('edit-title-symbol');
    header.addEventListener('mouseenter', () => {
        edit_symbol.addEventListener('click', () => {
            header_text.innerHTML = document.getElementById(`rename-${page}-form-div`).innerHTML;
        });
        edit_symbol.style.display = 'inline-block';
    });
    header.addEventListener('mouseleave', () => edit_symbol.style.display = 'none');   
}

function set_enable_scrolling_buttons() {
    // Enable scrolling when opening modal windows
    const open_modal_buttons = document.getElementsByClassName('open-modal-button');
    Array.from(open_modal_buttons).forEach(button => {
        button.addEventListener('click', () => enable_scrolling());
    })
}

function set_disable_scrolling_buttons() {
    // Disable scrolling back when closing modal windows
    const close_header_buttons = document.getElementsByClassName('close-header-button');
    const close_footer_buttons = document.getElementsByClassName('close-footer-button');
    Array.from(close_header_buttons).forEach(button => {
        button.addEventListener('click', () => disable_scrolling());
    })
    Array.from(close_footer_buttons).forEach(button => {
        button.addEventListener('click', () => disable_scrolling());
    })
}

function adjust_textarea_height(textarea) {
    // Set min height of textarea
    const min_rows = 2;

    // Calculate the number of rows needed based on the textarea's scrollHeight
    const calculatedRows = Math.max(min_rows, Math.ceil(textarea.scrollHeight / 20));

    // Update the rows attribute of the textarea
    textarea.rows = calculatedRows;
    textarea.style.resize = 'none';
}

function toggle_between_forget_password_forms() {
    // Get both forms
    const first_form = document.getElementById('first-form');
    const second_form = document.getElementById('second-form');

    // Hide one and show other
    if (second_form.style.display === 'none') {
        first_form.style.display = 'none';
        second_form.style.display = '';
    }
    else {
        second_form.style.display = 'none';
        first_form.style.display = '';
    }
}
