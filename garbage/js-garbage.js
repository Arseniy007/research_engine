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