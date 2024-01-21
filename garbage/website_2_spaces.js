// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    let dropdowns = document.getElementsByClassName("dropdown-content");
    for (let i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

function openNav() {
  // Open sidenav 
  const nav = document.querySelector(".sidenav");
  nav.style.width = "100%";
  nav.style.textAlign = 'center';
  nav.querySelector('#sidenav-closed-view').style.display = 'none';
  //nav.querySelector('#sidenav-full-view').style.display = 'block';

  // Load content
  load_index_data();
}

function closeNav() {
  // SMake sidenav full-width
  const nav = document.querySelector(".sidenav");
  nav.style.width = "240px";
  nav.style.textAlign = 'left';
  nav.querySelector('#sidenav-full-view').style.display = 'none';
  nav.querySelector('#sidenav-closed-view').style.display = 'block';
}

function dropdown_spaces() {
  document.getElementById("spaces-dropdown").classList.toggle("show");
}

function dropdown_papers() {
  document.getElementById("papers-dropdown").classList.toggle("show");
}

function dark_mode_toggle() {
  document.body.classList.toggle("dark-mode");
}

function load_index_data() {

  // API route for loading index content
  const url = '/index_loader';

  // Send request
  fetch(url)
  .then(function(response) {
    // When the page is loaded convert it to text
    return response.text()
  })
  .then(function(html) {
    // Initialize the DOM parser
    let parser = new DOMParser();

    // Parse the text
    let author_field_page = parser.parseFromString(html, "text/html");

    // Return author-field-div
    return author_field_page.querySelector('.form-body');
  })












  const empty_div = document.querySelector('#sidenav-full-view');






  
}