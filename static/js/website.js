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
  const nav = document.querySelector(".sidenav");
  nav.style.width = "100%";
  nav.style.textAlign = 'center';
  nav.querySelector('#close-nav-button').style.display = 'block';
}

function closeNav() {
  const nav = document.querySelector(".sidenav");
  nav.style.width = "240px";
  nav.style.textAlign = 'left';
  nav.querySelector('#close-nav-button').style.display = 'none';
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
