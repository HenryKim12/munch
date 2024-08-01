const apiClient = require("../api/apiClient");
const client = apiClient("recommendation")

const getContentRecommendation = async (req, res) => {
    try {
        const { user_id } = req.params
        response = await client.get(`/recommend/content/${user_id}`)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const getCollabRecommendation = async (req, res) => {
    try {
        // const { user_id } = req.params
        response = await client.get("/recommend/collab")
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

module.exports = {
    getContentRecommendation,
    getCollabRecommendation
}