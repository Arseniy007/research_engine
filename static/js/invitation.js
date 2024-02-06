document.addEventListener('DOMContentLoaded', function() {

    set_index_form_validation(document);

    // Prepopulate form fields
    const invitation_code = document.querySelector('#invitation-code');
    if (invitation_code) {
        document.querySelector('#code-field').value = invitation_code.innerHTML;
    }
    const share_sources_code = document.querySelector('#share-sources-code');
    if (share_sources_code) {
        document.querySelector('#sources-code-field').value = share_sources_code.innerHTML;
    }    
});
