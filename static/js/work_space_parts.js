document.addEventListener('DOMContentLoaded', function() {

    const space_id = document.querySelector('#space_id').innerHTML;
    const comment_form = document.querySelector('#comment_form');
    const note_form = document.querySelector('#note_form');
    const link_form = document.querySelector('#link_form');

    note_form.addEventListener('submit', event => {
        event.preventDefault();
        leave_note(note_form, space_id);
      });

    link_form.addEventListener('submit', event => {
        event.preventDefault();
        add_link(link_form, space_id);
      });

    comment_form.addEventListener('submit', event => {
        event.preventDefault();
        leave_comment(comment_form, space_id);
      });

});

function alter_comment(comment_id) {

    // Alter-comment view url
    const url = `/alter_comment/${comment_id}`;

    // TODO

}

function alter_note(note_id) {

    // Alter-note view url
    const url = `/alter_note/${note_id}`;

    // TODO

}

function alter_link(link_id) {

    // Alter-link view url
    const url = `/alter_link/${link_id}`;

    // TODO

}

function leave_note(form, space_id) {

    // Leave-note view url
    const url = `/leave_note/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            
            console.log(result.new_note);
            // TODO!
            // What to do?
            
        }
        else {
           redirect(result.url)
       }
    });
}

function leave_comment(form, space_id) {

    // Leave-comment view url
    const url = `/leave_comment/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            
            console.log(result.comment);
            // TODO!
            // What to do?
            
        }
        else {
           redirect(result.url)
       }
    });
}

function add_link(form, space_id) {

    // Add-link view url
    const url = `/add_link/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            
            console.log(result.link_name);
            // TODO!
            // What to do?
        }
        else {
            redirect(result.url)
        }
    });
}

function delete_comment(comment_id) {

    // Delete-comment view url
    const url = `/delete_comment/${comment_id}`;

    // Send GET request
    fetch(url)
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Remove comment
            document.querySelector(`#comment_${comment_id}`).remove();
        }
        else {
            console.log("error")
        }
    });
    // TODO: animation!
}

function delete_note(note_id) {

    // Delete-note view url
    const url = `/delete_note/${note_id}`;

    // Send request to delete_note view
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Remove comment
            document.querySelector(`#note_${note_id}`).remove();
        }
        else {
            console.log("error")
        }
    });
    // TODO: animation!
}

function delete_link(link_id) {

    // Delete-link view url
    const url = `/delete_link/${link_id}`;

    // Send request to delete_link view
    fetch(url)
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Remove comment
            document.querySelector(`#link_${link_id}`).remove();
        }
        else {
            console.log("error")
        }
    });
    // TODO: animation!
}

function redirect(url) {
    // Imitate django redirect func
    window.location.replace(url)
}

function handleErrors(response, url) {
    if (!response.ok) {
        if (response.statusText === 'Forbidden') {
            redirect(url)
        }

        // TODO: other errors 
    }
    return response;
}