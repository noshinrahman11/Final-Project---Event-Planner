function apiRequest (path,obj) {
    axios.post(path, obj).then(
        (response) => {
            let result = response.data;
            console.log(result);
        },
        (error) => {
            console.log(error);
        }
    );
}

<script src="https://unpkg.com/ axios/dist/axios.min.js"></script>
