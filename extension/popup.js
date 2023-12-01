// popup.js
function savePassword() {
    // Get values from the form
    var website = document.getElementById('website').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Send a POST request to Flask web service
    fetch('http://localhost:5000/save_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ website, username, password }),
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

function retrievePassword() {
    // Get values from the form
    var website = document.getElementById('website').value;

    // Send a POST request to Flask web service
    fetch('http://localhost:5000/retrieve_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ website }),
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}
