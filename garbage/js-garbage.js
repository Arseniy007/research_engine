/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("sidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  
  /* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
  function closeNav() {
    document.getElementById("sidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }
  


    // Hide first form
    document.querySelector('#first_form').style.display = 'none';

    // Show second form
    document.querySelector('#second_form').style.display = 'block';


  const number_of_forms = all_forms.length;
  for (let i = 0; i < number_of_forms; i++) {
       all_forms[i].style.display = 'none';
  }


  const show_form_buttons = document.getElementsByClassName('show_form_button');
  const number_of_buttons = show_form_buttons.length;
  for (let i = 0; i < number_of_buttons; i++) {
      let button = show_form_buttons[i];
      button.addEventListener('click', () => show_and_load_form(`${button.id}_form`));
  }


  const forms = document.getElementsByClassName('source_form');
  const number_of_forms1 = forms.length;

  for (let i = 0; i < number_of_forms1; i++) {
      forms[i].addEventListener('submit', () => {
          count_and_set_authors_number(forms[i])
      })
  }

  const submit_buttons = document.getElementsByClassName('submit_button');
  const number_of_submit_buttons = submit_buttons.length;

  for (let i = 0; i < number_of_submit_buttons; i++) {
      const form_id = submit_buttons[i].parentNode.id;
      submit_buttons[i].addEventListener('click', () => get_lobby_endnotes(form_id));
  }


  for (let i = 0; i < delete_quote_buttons.length; i++) {
    let button = delete_quote_buttons[i];
    button.addEventListener('click', () => delete_quote(button.id));
}



const show_form_buttons1 = document.getElementsByClassName('show_form_button');
Array.from(show_form_buttons1).forEach(button => {
    button.addEventListener('click', () => show_and_load_form(`${button.id}_form`));
})


// Hide this form if button was clicked second time:
const button_id = form_id.split('_')[0];
const show_this_form_button = document.querySelector(`#${button_id}`);
show_this_form_button.addEventListener('click', () => {
    hide_all_forms();
    show_this_form_button.addEventListener('click', () => show_and_load_form(`${button_id}_form`));
})


return author_field_page.querySelector('.author-field').innerHTML;

return author_field_page.querySelector('.form-body').innerHTML;

//author_div.innerHTML = await render_author_field(number_of_authors);

    // Get form one more time (in order to full version)
    const form = document.querySelector(`#${form_id}`);




function alter_source_info1(form, source_id) {

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



function load_script (script_path) {

    const head = document.getElementsByTagName('head')[0];
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = script_path;
    head.appendChild(script);

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
            // Change space title tag

            console.log(result.reference);

      
            
        }
        else {
            redirect(result.url)
        }
    });
}


function open_source_file(source_file_id) {

    // Display source-file url
    const url = `/source_file/${source_file_id}`;

}


// Get all new forms
const alter_source_form = document.querySelector(`#alter-source-form-${source_id}`);
const alter_source_reference_form = document.querySelector(`#alter-reference-form-${source_id}`);


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


Array.from(forms).forEach(form => async function() {

        
            
})


function add_link_to_source(form, source_id) {

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
            return true;
        }
        else {
            redirect(result.url)
        }
    });
}

async function alter_source_reference(form, source_id) {

    // Alter-source-endnote view url
    const url = `/alter_source_reference/${source_id}`;

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


if (form.id === `alter-reference-form-${source_id}`) {

    // Set form validation
    if (!form.checkValidity()) {
        form.classList.add('was-validated')
    }
    else {
        await alter_source_reference(form, source_id);
        // I don't need to update references
    }
}

if (!forms.length) {
  
    console.log('no form was changed');
}

const add_link_form = document.querySelector('#link-form');

add_link_form.addEventListener('submit', event => {
    event.preventDefault();
    add_link_to_source(add_link_form, source_id);
  });


  const close_button = document.querySelector(`#close-source-button-${source_id}`);
  close_button.style.display = 'none';
  close_button.style.display = 'inline-block';



        // Get open-source-file-button to display file
        //const source_file_id = source_space_page.querySelector('#source-file-id').innerHTML;
        //const open_file_button = source_space_page.querySelector(`#open-source-file-button-${source_id}`);
        //if (open_file_button) {
           // open_file_button.href = `/source_file/${source_file_id}`;
       // }

        // Enable toggle between modals
        const next_button = source_footer_div.querySelector('#next');
        const previous_button = source_footer_div.querySelector('previous');

        const source_footer_div = document.querySelector(`#source-footer-div-${source_id}`);
        //source_footer_div.innerHTML= source_space_page.querySelector('#source-footer').innerHTML;

        function toggle_between_modals(source_number) {
            console.log('yes');
            const open_source_button = document.querySelector(`#open-modal-button-${source_number}`);
            open_source_button.click();
            open_source_button.click();
            open_source_button.click();
        }
        
        
        function connect_modals_to_sources() {
        
            const sources = document.getElementsByClassName('source-modal');
        
            Array.from(sources).forEach(source => {
                source.addEventListener('shown.bs.modal', () => {
        
                    const source_id = source.querySelector('#source-id').innerHTML;
                    load_and_show_source_space(source_id);
                })
            })
        }


function set_form_validation() {

    // Fetch all the forms
    const forms = document.querySelectorAll('.needs-validation')
    
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }
        form.classList.add('was-validated')
        }, false)
    })
    }

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))



// TODO
const result_text = `
APA: ${result.apa_endnote}
MLA: ${result.mla_endnote}`
document.querySelector('#result').innerHTML = result_text;

// Set validation for settings forms
const account_settings_forms = document.getElementsByClassName('account-settings-form');
Array.from(account_settings_forms).forEach(form => {
    form.addEventListener('change', function() {
        form.classList.add('was-changed')
    })
})

async function submit_settings_forms() {

    // Get all changed forms
    const forms = document.getElementsByClassName('was-changed');

    if (!forms.length) {
        // In case no form was changed
        return;
    }
    for await (const form of forms) {
        if (form.id === 'main-info-form') {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source main info
                if (!await update_user_main_info(form)) {
                    // Error case
                    return location.reload()
                }
            }
        }
        else if (form.id === 'change-password-form') {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source link
                if (!await change_user_password(form)) {
                    // Error case
                    return location.reload()
                }
            }
        }
    }
    return window.location.replace('/login')
}

async function update_user_main_info(form) {

    // Account settings view
    const url = '/account_settings';

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
            return false;
        }
    })
}

async function change_user_password(form) {

    // Account settings view
    const url = '/change_password';

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
            return false;
        }
    })
}


async function submit_settings_forms() {

    // Get all changed forms
    const forms = document.getElementsByClassName('was-changed');

    if (!forms.length) {
        // In case no form was changed
        return;
    }
    for await (const form of forms) {
        if (form.id === 'main-info-form') {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source main info
                if (!await update_user_main_info(form)) {
                    // Error case
                    return location.reload()
                }
            }
        }
        else if (form.id === 'change-password-form') {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source link
                if (!await change_user_password(form)) {
                    // Error case
                    return location.reload()
                }
            }
        }
    }
    return window.location.replace('/login')
}

async function update_user_main_info(form) {

    // Account settings view
    const url = '/account_settings';

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
            return false;
        }
    })
}

async function change_user_password(form) {

    // Account settings view
    const url = '/change_password';

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
            return false;
        }
    })
}

result_field.innerHTML = `APA:\n${result.reference.apa_endnote}\n\nMLA:\n${result.reference.mla_endnote}`


new_space_form.addEventListener('submit', event => {
    if (!new_space_form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        new_space_form.classList.add('was-validated');
    }
})

const index_forms = nav.getElementsByClassName('index-form');
    Array.from(index_forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
            }

        })
    })

    const create_space_form = nav.querySelector('#create-space-form');
    create_space_form.addEventListener('submit', event => {
        if (!create_space_form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            create_space_form.classList.add('was-validated');
        }
        else {
            event.preventDefault();
            create_new_work_space(create_space_form);
        }
    })


function redirect_to_index_with_error() {

    window.location.replace("");
    openNav();
    document.querySelector('#index-error-message').style.display = 'block';
}


document.querySelector('#save-changes-button').addEventListener('click', () => settings_form.submit());


const settings_form = document.querySelector('#settings-form');

document.querySelector('#save-changes-button').addEventListener('click', () => {
    if (!settings_form.checkValidity()) {
        settings_form.classList.add('was-validated');
    }
    else {
        settings_form.submit();
    }
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

function test(paper_id) {

    const header = document.querySelector('#header-text');
    let paper_title = header.innerHTML;
    paper_title = paper_title.replace(/\s/g, '');
    
    //header.style.display = 'none';

    let rename_field = document.createElement('input');
    rename_field.classList.add('form-control');
    rename_field.type = 'text';
    rename_field.value = paper_title;

    header.innerHTML = '';
    header.append(rename_field)




}


const settings_form1 = document.querySelector('#settings-form');
settings_form.addEventListener('submit', event => {
    if (!settings_form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }
    settings_form.classList.add('was-validated');
})


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

const rename_space_form = document.querySelector('#rename_space_form');
rename_space_form.addEventListener('submit', event => {
    event.preventDefault();
    rename_space(rename_space_form, space_id);
  });

  function rename_space(form, space_id) {

    // Rename-space url
    const url = `/rename_space/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => handleErrors(response, url))
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


document.querySelector('#reference-result-field-apa').innerHTML = result.reference.apa_endnote;
document.querySelector('#reference-result-field-mla').innerHTML = result.reference.apa_endnote;

const apa_field = document.querySelector('#reference-result-field-apa');
const mla_field = document.querySelector('#reference-result-field-mla');
apa_field.innerHTML = result.reference.apa_endnote;
mla_field.innerHTML = result.reference.apa_endnote;


async function auto_grow(textarea) {
    console.log('hi')
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

function delay(milliseconds){
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}


function adjust_textarea_height(textarea) {

    const min_rows = 2;

    const calculated_rows = Math.max(min_rows, Math.ceil(textarea.scrollHeight / 20));

    textarea.rows = calculated_rows;

}



//apa_field.innerHTML = result.reference.apa_endnote;
            //mla_field.value = result.reference.mla_endnote;

            //adjust_textarea_height(apa_field)
            //adjust_textarea_height(mla_field)

            //apa_field.dispatchEvent(new Event('input'));

            //apa_field.setAttribute("style", "height:" + (apa_field.scrollHeight) + "px;overflow-y:hidden;");
            //apa_field.addEventListener('input', auto_grow(apa_field), false)

            //apa_field.dispatchEvent(new Event('input', { bubbles: true }));


            //apa_field.style.height = (result.reference.apa_endnote.scrollHeight) + 'px;overflow-y:hidden';
            //mla_field.style.height = (result.reference.mla_endnote.scrollHeight) + 'px;overflow-y:hidden;';
  
            // TODO

function updateTextareaValue(textarea, value) {

    textarea.value = value;

    // Manually trigger the resizing logic
    adjust_textarea_height(textarea);
}


function receive_invitation(form, invitation_page=false) {

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
            let error_message;
            if (invitation_page) {
                error_message = document.querySelector('#invitation-error-message');
            }
            else {
                document.querySelector('#index-error-message');
            }
            error_message.querySelector('.error').innerHTML = result.message;
            error_message.style.display = 'block';
        }
    });
}


window.onscroll = function() {myFunction()};

const header = document.querySelector('#header');
let sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } 
    else {
        header.classList.remove("sticky");
    }
}

function dark_mode_toggle() {
    document.body.classList.toggle("dark-mode");
}


function hide_all_areas() {
    // Hide all parts of workspace
    document.querySelector('#sources-area').style.display = 'none';
    document.querySelector('#papers-area').style.display = 'none';
    document.querySelector('#links-area').style.display = 'none';
}

function show_sources_area() {
    hide_all_areas();
    document.querySelector('#sources-area').style.display = '';
}

function show_papers_area() {
    hide_all_areas();
    document.querySelector('#papers-area').style.display = '';
}

function show_links_area() {
    hide_all_areas();
    document.querySelector('#links-area').style.display = '';
}

async function invite_to_work_space(space_id) {

    // Get invitation code and link
    const answer = await get_invitation_code(space_id);

    // Render results inside opened modal
    document.querySelector('#invitation-link').innerHTML = answer.invitation_code;
    document.querySelector('#invitation-code').innerHTML = answer.invitation_code;
}

async function share_space_sources(space_id) {

    // Get sharing code and link
    const answer = await get_share_space_source_code(space_id);

    // Render results inside opened modal
    document.querySelector('#sources-code').innerHTML = answer.share_sources_code;
    document.querySelector('#sources-link').innerHTML = answer.share_sources_link;

}

async function share_space_sources1(space_id) {

    // Get sharing code and link
    const answer = await get_share_space_source_code(space_id);

    // Render results inside opened modal
    document.querySelector('#sources-code').innerHTML = answer.share_sources_code;
    document.querySelector('#sources-link').innerHTML = answer.share_sources_link;

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


if (area_id === 'actions-area') {
    // Disable scrolling
    document.getElementsByTagName('body')[0].classList.add('stop-scrolling');
}
else if (area_id === 'members-area') {
    if (area.getElementsByClassName('member-card').length <= 3) {
        // Disable scrolling if there is no members at workspace
        document.getElementsByTagName('body')[0].classList.add('stop-scrolling');
    }
}
else if (area_id === 'papers-area') {
    if (area.getElementsByClassName('paper-card').length <= 4) {
        // Disable scrolling if there is no members at workspace
        document.getElementById('content').classList.add('stop-scrolling');

        //document.getElementsByTagName('body')[0].classList.add('stop-scrolling');
    }
}


// Show and hide rename paper form
const header1 = document.querySelector('#header');
const header_text = document.querySelector('#header-text');
const edit_symbol = document.querySelector('#edit-title-symbol');
header.addEventListener('mouseenter', () => {
    edit_symbol.addEventListener('click', () => {
        header_text.innerHTML = document.querySelector('#rename-paper-form-div').innerHTML;
    });
    edit_symbol.style.display = 'inline-block';
});
header.addEventListener('mouseleave', () => edit_symbol.style.display = 'none');


const source_id = document.querySelector('#source-id').innerHTML;

// Show and hide source settings form
const header2 = document.querySelector('#header');
const eeedit_symbol = document.querySelector('#edit-title-symbol');
header.addEventListener('mouseenter', () => {
    edit_symbol.addEventListener('click', () => {
        document.getElementById(`source-space-${source_id}`).style.display = 'none';
        document.getElementById(`source-settings-${source_id}`).style.display = '';
    });
    edit_symbol.style.display = 'inline-block';
});
header.addEventListener('mouseleave', () => edit_symbol.style.display = 'none'); 


function load_main_paper_area() {
    // Check if paper has files
    const last_file_id = document.querySelector('#last-file-id').innerHTML;
    if (last_file_id) {
        // Load paper statistics
        get_paper_file_info(last_file_id);
    }
    else {
        // If there are no files - TODO

    }
}

const sourceww_id = document.querySelector('#source-id').innerHTML;
const new_quote_form = document.querySelector('#new_quote_form');
//const alter_quote_form = document.querySelector('#alter_quote_form');
const delete_quote_buttons = document.getElementsByClassName('delete_quote_buttons');

new_quote_form.addEventListener('submit', event => {
    event.preventDefault();
    add_quote(new_quote_form, source_id);
  });

//alter_quote_form.addEventListener('submit', event => {
  //  event.preventDefault();
   // alter_quote(alter_quote_form, source_id);
//  });

Array.from(delete_quote_buttons).forEach(button => {
    button.addEventListener('click', () => delete_quote(button.id));
})

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


function mark_source_as_checked(source_id) {
    // Get right card
    const source_card = document.getElementById(`source-card-${source_id}`);

    // Check or uncheck source checkbox
    const check_box = source_card.querySelector(`#source-checkbox-${source_id}`);
    if (check_box.checked === false) {
        check_box.checked = true;
        source_card.classList.add('checked-item');
    }
    else {
        check_box.checked = false;
        source_card.classList.remove('checked-item');
    }
}

function choose_all_sources() {
    // Get all source cards
    const all_sources = document.getElementsByClassName('source-card');

    // Check all sources
    Array.from(all_sources).forEach(source => {
        const check_box = source.getElementsByClassName('source-checkbox')[0];
        check_box.checked = true;
        source.classList.add('checked-item');
    })
}

function check_password(form_name) {

    // Get new password and its confirmation
    const password = document.forms[form_name]["password"].value;
    const confirmation = document.forms[form_name]["confirmation"].value;
    const length = password.length;
    let digit = false;
    let upper = false;

    // Show error message if password and confirmation don't match
    if (password != confirmation) {

        return false;
    }

    for (let i = 0; i < length; i++) {

        let char = password[i];

        // Check if at least one character is digit
        if (char >= '0' && char <= '9') {

            digit = true;
        }
        // Check if at least one character is uppercase
        else if (char === char.toUpperCase()) {

            upper = true;
        }
    }

    if (!(digit && upper && length > 5)) {

        return false;
    }

    // Submit the form if password is ok
    return true;
}

function enable_source_rename_form() {
    // Show and hide source settings form
    const header = document.querySelector('#header');
    const edit_symbol = document.querySelector('#edit-title-symbol');
    header.addEventListener('mouseenter', () => {
        edit_symbol.addEventListener('click', () => {
            document.getElementById('settings-area-button').click();
        });
        edit_symbol.style.display = 'inline-block';
    });
    header.addEventListener('mouseleave', () => edit_symbol.style.display = 'none'); 
}



function delete_source(source_id) {
    // Get delete button and ask user for conformation
    const delete_button = document.querySelector(`#delete-source-button-${source_id}`);
    delete_button.innerHTML = "Are you sure?";

    delete_button.addEventListener('click', () => {
        // Remove source card from page
        document.querySelector(`#close-source-settings-button-${source_id}`).click();
        document.querySelector(`#close-source-modal-button-${source_id}`).click();
        document.querySelector(`#source-card-${source_id}`).remove();

        // Send request
        const url = `/delete_source/${source_id}`;
        fetch(url)
        .then(response => handleErrors(response, url))
    })
}

async function submit_source_forms(source_id) {

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
                if (!await alter_source_info(form, source_id)) {
                    // Error case
                    return show_form_error_message();
                }
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
                if (!await add_link_to_source(form, source_id)) {
                    // Error case
                    return show_form_error_message();
                }
            }
        }
        else if (form.id === `upload-file-form-${source_id}`) {
            // Save new source file
            if (!await upload_source_file(form, source_id)) {
                // Error case
                return show_form_error_message();
            }
        }
    }
    // Update source space in case of success
    load_and_show_source_space(source_id);
    document.querySelector(`#close-source-settings-button-${source_id}`).click();
}

async function alter_source_info(form, source_id) {

    // Alter-source-info view url
    const url = `/alter_source_info/${source_id}`;

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return false;
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
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return false;
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
            return false;
        }
    });
}

function show_form_error_message() {
    document.querySelector('.form-error-message').style.display = 'block';
}

function show_or_hide_source_settings(source_id) {
    // Get main divs
    const source_div = document.querySelector(`#source-space-${source_id}`);
    const source_settings_div = document.querySelector(`#source-settings-${source_id}`);
    // Get all buttons
    const btn_close_button = document.querySelector(`#btn-close-${source_id}`);
    const close_modal_button = document.querySelector(`#close-source-modal-button-${source_id}`);
    const edit_button = document.querySelector(`#show-source-settings-button-${source_id}`);
    const close_settings_button = document.querySelector(`#close-source-settings-button-${source_id}`);
    const delete_button = document.querySelector(`#delete-source-button-${source_id}`);
    const link_button = document.querySelector(`#source-link-button-${source_id}`);
    const open_file_button = document.querySelector(`#open-source-file-button-${source_id}`);
    const expand_button = document.querySelector(`#expand-button-${source_id}`);

    // Open source settings
    if (source_settings_div.style.display === 'none') {
        source_div.style.display = 'none';
        source_settings_div.style.display = 'block';

        // Change all buttons
        edit_button.style.display = 'none';
        close_modal_button.style.display = 'none';
        btn_close_button.style.display = 'none';
        expand_button.style.display = 'none';
        close_settings_button.style.display = 'inline-block';
        delete_button.style.display = 'inline-block';

        if (open_file_button) {
            open_file_button.style.display = 'none';
        }
        if (link_button) {
            link_button.style.display = 'none';
        }        
    }
    // Close source settings
    else {
        source_settings_div.style.display = 'none';
        source_div.style.display = 'block';
        // Change all buttons
        close_settings_button.style.display = 'none';
        delete_button.innerHTML = 'Delete source';
        delete_button.style.display = 'none';
        edit_button.style.display = 'inline-block';
        close_modal_button.style.display = 'inline-block';
        expand_button.style.display = 'inline-block';
        btn_close_button.style.display = 'block';

        if (open_file_button) {
            open_file_button.style.display = 'inline-block';
        }
        if (link_button) {
            link_button.style.display = 'inline-block';
        }
    }
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

function load_and_show_new_source_space(url) {

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

        // Get div for pasting (the one with submitted form)
        const new_source_div = document.querySelector('#new-source-div');

        // Past source space header
        const source_space_header = source_space_page.querySelector('#source-space-header');
        document.querySelector('#new-source-label').innerHTML = source_space_header.innerHTML;

        // Past source footer
        const old_footer =  document.querySelector('#new-source-footer');
        const source_space_footer = source_space_page.querySelector('#hidden-source-footer');
        old_footer.classList.add('source-footer');
        old_footer.innerHTML = source_space_footer.innerHTML;

        // Sat new ids
        const source_id = source_space_page.querySelector('#source-id').innerHTML;
        document.querySelector('#new-source-label').id = `source-space-label-${source_id}`;
        document.querySelector('#btn-new-source-close-button').id = `btn-close-${source_id}`
        document.querySelector('#new-source-div').id = `source-space-div-${source_id}`;

        // Past fetched body
        new_source_div.innerHTML = source_space_page.querySelector('#source-space-div').innerHTML;

        // Set validation for source-edit-forms
        const edit_forms = document.getElementsByClassName('edit-form');
        Array.from(edit_forms).forEach(form => {
            form.addEventListener('change', function() {
                form.classList.add('was-changed')
            })
        })
    })
}

function load_and_show_new_source_space(url) {

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

        // Get div for pasting (the one with submitted form)
        const new_source_div = document.querySelector('#new-source-div');

        // Past source space header
        const source_space_header = source_space_page.querySelector('#source-space-header');
        document.querySelector('#new-source-label').innerHTML = source_space_header.innerHTML;

        // Past source footer
        const old_footer =  document.querySelector('#new-source-footer');
        const source_space_footer = source_space_page.querySelector('#hidden-source-footer');
        old_footer.classList.add('source-footer');
        old_footer.innerHTML = source_space_footer.innerHTML;

        // Sat new ids
        const source_id = source_space_page.querySelector('#source-id').innerHTML;
        document.querySelector('#new-source-label').id = `source-space-label-${source_id}`;
        document.querySelector('#btn-new-source-close-button').id = `btn-close-${source_id}`
        document.querySelector('#new-source-div').id = `source-space-div-${source_id}`;

        // Past fetched body
        new_source_div.innerHTML = source_space_page.querySelector('#source-space-div').innerHTML;

       
    })
}



if (result.status === 'ok') {
    // Fill opened div with new source space
    load_and_show_new_source_space(result.new_source_id);
}
else {
    // Redirect back to work space view in case of error
    window.location.replace(result.url)
}

function load_and_show_new_source_space(source_id) {

    // Source page view url
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
        const source_space = parser.parseFromString(html, "text/html");

        // Get source data
        const source_header = source_space.querySelector('#source-header').innerHTML;
        const source_body = source_space.querySelector('#new-source-body').innerHTML;
        const source_footer = source_space.querySelector('#new-source-footer').innerHTML;

        // Past data
        document.getElementById('new-source-label').innerHTML = source_header;
        document.getElementById('new-source-div').innerHTML = source_body;
        document.getElementById('new-source-footer').innerHTML =  source_footer;       
    })
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
