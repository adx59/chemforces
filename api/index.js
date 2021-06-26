const express = require("express");
const bodyParser = require("body-parser");

var app = express();
app.use(bodyParser);

const problem = require("./routers/problem.js");
const random = require("./routers/random.js");
app.use("/problem", problem);
app.use("/random", random);

app.listen(80);
