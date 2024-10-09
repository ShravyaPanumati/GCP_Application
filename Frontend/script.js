// Function to fetch the backend URL from the ConfigMap or an endpoint
async function fetchConfig() {
    try {
        const response = await fetch('/path/to/config'); // Replace with your config endpoint
        const configData = await response.json();
        return configData.FLASK_SERVER_URL; // This is where you retrieve the URL from your config
    } catch (error) {
        console.error('Error fetching config:', error);
        return 'http://localhost:5000'; // Fallback URL for local development
    }
}

// Initialize the application
async function initApp() {
    const backendUrl = await fetchConfig();

    // Handle Insert
    document.getElementById('insertForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const value1 = document.getElementById('value1').value;
        const value2 = document.getElementById('value2').value;

        fetch(`${backendUrl}/insert`, {  // Use the dynamic URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ value1: value1, value2: value2 })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById('insertResult').innerHTML = `<p style="color: green;">${data.message}</p>`;
            } else {
                document.getElementById('insertResult').innerHTML = `<p style="color: red;">${data.error}</p>`;
            }
        })
        .catch((error) => {
            document.getElementById('insertResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });

    // Handle Fetch Values
    document.getElementById('fetchButton').addEventListener('click', function () {
        fetch(`${backendUrl}/fetch`, {  // Use the dynamic URL
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            let output = '<table><tr><th>ID</th><th>Value 1</th><th>Value 2</th></tr>';
            data.forEach(function (row) {
                output += `<tr><td>${row.id}</td><td>${row.value1}</td><td>${row.value2}</td></tr>`;
            });
            output += '</table>';

            document.getElementById('fetchResult').innerHTML = output;
        })
        .catch((error) => {
            document.getElementById('fetchResult').innerHTML = `<p style="color: red;">Error fetching values: ${error.message}</p>`;
        });
    });

    // Handle File Upload
    document.getElementById('uploadForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            document.getElementById('uploadResult').innerHTML = '<p style="color: red;">Please select a file to upload.</p>';
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch(`${backendUrl}/upload`, {  // Use the dynamic URL
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById('uploadResult').innerHTML = `<p style="color: green;">${data.message}</p>`;
            } else {
                document.getElementById('uploadResult').innerHTML = `<p style="color: red;">${data.error}</p>`;
            }
        })
        .catch((error) => {
            document.getElementById('uploadResult').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });
}

// Call the function to initialize the app
initApp();
