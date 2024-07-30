const { json } = require("express");
const apiClient = require("../api/apiClient");
const client = apiClient("user")

const getUsers = async (req, res) => {
    try {
        response = await client.get("/users")
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const getUserById = async (req, res) => {
    try {
        const { user_id } = req.params
        response = await client.get(`/users/${user_id}`)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const createUser = async (req, res) => {
    try {
        const postData = req.body
        response = await client.post("/users", postData)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const deleteUser = async (req, res) => {
    try {
        const { user_id } = req.params
        response = await client.delete(`/users/${user_id}`)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const updateUser = async (req, res) => {
    try {
        const { user_id } = req.params
        response = await client.put(`/users/${user_id}`)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const getUserRestaurants = async (req, res) => {
    try {
        const { user_id } = req.params
        response = await client.get(`/users/${user_id}/restaurants`)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const addUserRestaurant = async (req, res) => {
    try {
        const { user_id } = req.params
        const postData = req.body
        response = await client.post(`/users/${user_id}/restaurants`, postData)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const deleteUserRestaurant = async (req, res) => {
    try {
        const { user_id, restaurant_id } = req.params
        response = await client.delete(`/users/${user_id}/restaurants/${restaurant_id}`)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

const updateUserRestaurant = async (req, res) => {
    try {
        const { user_id, restaurant_id } = req.params
        const postData = req.body
        response = await client.put(`/users/${user_id}/restaurants/${restaurant_id}`, postData)
        res.status(200).json(response.data)
    } catch (error) {
        res.status(400).json(error.message)
    }
}

module.exports = {
    getUsers,
    getUserById,
    createUser,
    deleteUser,
    updateUser,
    getUserRestaurants,
    addUserRestaurant,
    deleteUserRestaurant,
    updateUserRestaurant
}