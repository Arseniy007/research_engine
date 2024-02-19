document.addEventListener('DOMContentLoaded', function() {
    enable_nav_links();
    disable_scrolling();
    set_form_validation();
    set_huge_icon_margin();
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

function set_huge_icon_margin() {
    // Calculate scroll height of reference field and set top margin for left icon
    const calculated_height = document.getElementsByClassName('reference-huge')[0].scrollHeight / 6;
    document.getElementsByClassName('source-type-icon-huge')[0].style.marginTop = `${calculated_height}px`;
}
