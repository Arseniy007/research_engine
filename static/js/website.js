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
  nav.querySelector('#sidenav-full-view').style.display = 'block';

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

  // TODO

  
}