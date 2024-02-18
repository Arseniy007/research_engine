document.addEventListener('DOMContentLoaded', function() {

    enable_nav_links();
    enable_source_rename_form();

});


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
