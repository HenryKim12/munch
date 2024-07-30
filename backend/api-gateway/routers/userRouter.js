const userController = require("../controllers/userController")

const express = require("express")
const router = express.Router()

router.get("/", userController.getUsers);
router.get("/:user_id", userController.getUserById);
router.post("/", userController.createUser);
router.delete("/:user_id", userController.deleteUser);
router.put("/:user_id", userController.updateUser);

router.get("/:user_id/restaurants", userController.getUserRestaurants);
router.post("/:user_id/restaurants", userController.addUserRestaurant);
router.delete("/:user_id/restaurants/:restaurant_id", userController.deleteUserRestaurant);
router.put("/:user_id/restaurants/:restaurant_id", userController.updateUserRestaurant);

module.exports = router