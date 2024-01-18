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

function dropdown_spaces() {
  document.getElementById("spaces-dropdown").classList.toggle("show");
}

function dropdown_papers() {
  document.getElementById("papers-dropdown").classList.toggle("show");
}

function dark_mode_toggle() {
  document.body.classList.toggle("dark-mode");
}
