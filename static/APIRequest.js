// APIRequest.js

// Function to make an API request
function apiRequest(path, obj, callback) {
    axios.post(path, obj)
        .then((response) => {
            let result = response.data;
            callback(result); // Call the callback function with the fetched data
        })
        .catch((error) => {
            console.log(error);
        });
}
