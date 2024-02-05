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