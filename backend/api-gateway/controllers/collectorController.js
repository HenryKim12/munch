const apiClient = require("../api/apiClient");
const client = apiClient("collector")

const getRestaurants = async (req, res) => {
    try {
        const response = await client.get("/restaurants")
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const getRestaurantById = async (req, res) => {
    try {
        const { restaurant_id } = req.params
        const response = await client.get(`/restaurants/${restaurant_id}`)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const getUserRatedRestaurants = async (req, res) => {
    try {
        // const response = await client.get("/restaurants/rated")
        // res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

module.exports = {
    getRestaurants,
    getRestaurantById,
    getUserRatedRestaurants
}