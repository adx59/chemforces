const express = require("express");

const probIndex = require("../../sets/index.json")

var router = express.Router();

router.get("/", async function (req, res) {
    return res.status(400).sendFile("404.png", {root: "../sets/" });
});

router.get("/:year/:prob", async function (req, res) {
    var links = probIndex[`${req.params.year}_${req.params.prob}`]
    if (!links) return res.status(404).send("couldn't find that problem")
    
    return res.status(200).sendFile(links.page, { root: "../" });
});

module.exports = router