const collectorController = require("../controllers/collectorController")

const express = require("express")
const router = express.Router()

router.get("/", collectorController.getRestaurants);

module.exports = router