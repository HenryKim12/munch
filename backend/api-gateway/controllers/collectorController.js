const apiClient = require("../api/apiClient");
const client = apiClient("collector")

const getRestaurants = async (req, res) => {
    const response = await client.get("/")
    console.log(response.status)
}

module.exports = {
    getRestaurants,

}