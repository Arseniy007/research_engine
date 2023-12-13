document.addEventListener('DOMContentLoaded', function() {

    // Get follow button and add functionality to it
    const profile_id = document.querySelector('#profile_id').innerHTML;
    document.querySelector('#follow_button').addEventListener('click', () => follow(profile_id));

});

function follow(profile_id) {

    const url = `/follow/${profile_id}`

    // Send request to follow-view
    fetch(url)
    .then(response => response.json())
    .then(result => {

        // Get right text for follow button
        let button_text;
        if (result.status === 'not followed') {
            button_text = 'Follow';
        }
        else {
            button_text = 'Unfollow';
        }
        // Update number of followers
        document.querySelector('#follow_button').innerHTML = button_text;
        document.querySelector('#number_of_followers').innerHTML = `Number of followers: ${result.number_of_followers}`;
    });
}
