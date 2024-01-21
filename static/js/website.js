const gray = '#222222';
const black = '#111';

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

function dropdown_spaces() {
    document.getElementById("spaces-dropdown").classList.toggle("show");
}

function dropdown_papers() {
    document.getElementById("papers-dropdown").classList.toggle("show");
}

function dark_mode_toggle() {
    document.body.classList.toggle("dark-mode");
}

async function openNav() {
    // Open sidenav 
    const nav = document.querySelector(".sidenav");
    nav.style.width = "100%";
    nav.style.textAlign = 'center';
    nav.style.background = gray;
    nav.querySelector('#sidenav-closed-view').style.display = 'none';

    // Load content
    const index_content = await load_index_data();
    nav.querySelector('#index-container').innerHTML = index_content.innerHTML;

    // Set form validation
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
    // Show everything
    nav.querySelector('#sidenav-full-view').style.display = 'block';
}

function closeNav() {
    // SMake sidenav full-width
    const nav = document.querySelector(".sidenav");
    nav.style.width = "240px";
    nav.style.textAlign = 'left';
    nav.style.background = black;
    nav.querySelector('#sidenav-full-view').style.display = 'none';
    nav.querySelector('#sidenav-closed-view').style.display = 'block';
}

async function load_index_data() {

    // API route for loading index content
    const url = '/index';

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
