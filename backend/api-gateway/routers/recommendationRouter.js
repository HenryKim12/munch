const recommendationController = require("../controllers/recommendationController")

const express = require("express")
const router = express.Router()

router.get("/content/:user_id", recommendationController.getContentRecommendation);
router.get("/collab", recommendationController.getCollabRecommendation);

module.exports = router