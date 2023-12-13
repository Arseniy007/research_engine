document.addEventListener('DOMContentLoaded', function() {

    

});


function alter_comment(comment_id) {

    const url = `/alter_comment/${comment_id}`;

}


function delete_comment(comment_id) {

    // Send request to delete_comment view
    fetch(`/delete_comment/${comment_id}`)
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

    // Send request to delete_note view
    fetch(`/delete_note/${note_id}`)
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

    // Send request to delete_link view
    fetch(`/delete_link/${link_id}`)
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
