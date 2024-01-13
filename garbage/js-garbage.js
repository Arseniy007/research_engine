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

            // TODO
            
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
    // TODO
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
