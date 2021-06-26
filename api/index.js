const express = require("express");
const morgan = require("morgan");

var app = express();

const problem = require("./routes/problem.js");
const page = require("./routes/page.js")
const random = require("./routes/random.js");

app.use(morgan("tiny"));

app.use("/problem", problem);
app.use("/random", random);
app.use("/page", page);

// debug
app.listen(3000);
