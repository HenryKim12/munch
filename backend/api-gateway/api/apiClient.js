const axios = require("axios")

const apiClient = (service) => {
    let url;
    if (service == "collector") {
        url = "http://127.0.0.1:5001"
    } else if (service == "user") {
        url = "http://127.0.0.1:5002"
    } else if (service == "recommendation") {
        url = "http://127.0.0.1:5003"
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