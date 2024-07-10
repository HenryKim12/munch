const axios = require("axios")

const apiClient = (service) => {
    let url;
    if (service == "collector") {
        url = "http://127.0.0.1:5000"
    }

    client = axios.create({
        baseURL: url,
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true,
    });
    
    return client
} 

module.exports = apiClient;