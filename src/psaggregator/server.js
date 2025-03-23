import { handler } from "./build/handler.js";
import express from "express";
import morgan from "morgan";

const app = express();

app.use(morgan("[:date[iso]] :remote-addr :method :url HTTP/:http-version :status :res[content-length] - :response-time ms"));

app.use(handler);

app.listen(3000, () => {
    console.log("listening on port 3000");
});
