require("dotenv").config();
var cors = require("cors");

const express = require("express");
const app = express();
app.use(cors())

// middleware
app.use(express.json());
app.use((req, res, next) => {
    console.log(req.path, req.method);
    next();
})

app.listen(process.env.PORT, () => {
    console.log(`listening on port ${process.env.PORT}`);
})