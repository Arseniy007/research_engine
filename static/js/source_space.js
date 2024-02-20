document.addEventListener('DOMContentLoaded', () => {
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
    const calculated_height = document.getElementById('reference-huge').scrollHeight / 6;
    document.getElementById('source-type-icon-huge').style.marginTop = `${calculated_height}px`;
}
