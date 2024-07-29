require("dotenv").config();
var cors = require("cors");

const collectorRouter = require("./routers/collectorRouter")
const userRouter = require("./routers/userRouter")
const recommendationRouter = require("./routers/recommendationRouter")

const express = require("express");
const app = express();
app.use(cors())

// middleware
app.use(express.json());
app.use((req, res, next) => {
    console.log(`[${new Date()}] ${req.method}: ${req.path}`);
    next();
})

app.use("/collector", collectorRouter)
app.use("/user", userRouter)
app.use("/recommendation", recommendationRouter)

app.listen(process.env.PORT, () => {
    console.log(`listening on port ${process.env.PORT}`);
})