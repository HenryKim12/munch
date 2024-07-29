const userController = require("../controllers/userController")

const express = require("express")
const router = express.Router()

router.get("/", userController.getUsers);
router.get("/:user_id", userController.getUserById);
router.post("/", userController.createUser);
router.delete("/:user_id", userController.deleteUser);
router.put("/:user_id", userController.updateUser);
router.get("/restaurants/:user_id", userController.getUserRestaurants);
router.post("/restaurants", userController.addUserRestaurant);
router.delete("/restaurants/:user_id/:restaurant_id", userController.deleteUserRestaurant);
router.put("/restaurants/:user_id/:restaurant_id", userController.updateUserRestaurant);

module.exports = router