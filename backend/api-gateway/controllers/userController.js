const apiClient = require("../api/apiClient");
const client = apiClient("user")

const getUsers = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const getUserById = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const createUser = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const deleteUser = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const updateUser = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const getUserRestaurants = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const addUserRestaurant = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const deleteUserRestaurant = async (req, res) => {
    try {

    } catch (error) {
        res.status(400).json(error.message)
    }
}

const updateUserRestaurant = async (req, res) => {
    try {

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