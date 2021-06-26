const express = require("express");

const probIndex = require("../../sets/index.json")

var router = express.Router();

router.get("/", async function (req, res) {
    var pbs = Object.keys(probIndex);
    var pb = pbs[Math.floor(Math.random() * pbs.length)]

    return res.status(200).send({
        year: pb.split("_")[0],
        prob: pb.split("_")[1]
    });
})

module.exports = router