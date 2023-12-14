document.addEventListener('DOMContentLoaded', function() {

    const space_id = document.querySelector('#space_id').innerHTML;
    const rename_form = document.querySelector('#rename_form');

    rename_form.addEventListener('submit', event => {
        event.preventDefault();
        rename_space(rename_form, space_id);
      })

});


function rename_space(form, space_id) {

    // Rename-space view url
    const url = `/rename_space/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Change space title tag
            document.querySelector('#space_title').innerHTML = result.new_title;
        }
        else {
            redirect(result.url)
        }
    });
}


function redirect(url) {
    // Imitate django redirect func
    window.location.replace(url)
}
