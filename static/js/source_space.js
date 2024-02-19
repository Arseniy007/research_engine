document.addEventListener('DOMContentLoaded', function() {

    enable_nav_links();
    disable_scrolling();
    set_form_validation();
    set_enable_scrolling_buttons();
    set_disable_scrolling_buttons();
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
