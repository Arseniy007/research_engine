document.addEventListener('DOMContentLoaded', function() {

    enable_nav_links();
    disable_scrolling();
    set_form_validation();
    set_enable_scrolling_buttons();
    set_disable_scrolling_buttons();
    




    enable_source_rename_form();



});

function show_source_area(area_id) {
    // Hide all areas first then show one
    hide_all_areas('source');
    const area = document.getElementById(area_id);
    if (!area) {
        return;
    }
    disable_scrolling();
    area.style.display = '';
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
