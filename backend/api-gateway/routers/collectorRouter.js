const collectorController = require("../controllers/collectorController")

const express = require("express")
const router = express.Router()

router.get("/restaurants", collectorController.getRestaurants);
router.get("/restaurants/:restaurant_id", collectorController.getRestaurantById)
router.get("/restaurants/rated", collectorController.getUserRatedRestaurants)

module.exports = router