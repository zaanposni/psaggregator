import { handler } from "./build/handler.js";
import express from "express";
import { expressAnalytics, Config } from "node-api-analytics";
import morgan from "morgan";

const app = express();

if (process.env.PRIVATE_API_ANALYTICS_KEY) {
    const apiAnalyticsConfig = new Config();
    apiAnalyticsConfig.getPath = (req) => {
        if (req.path.startsWith("/api/video/")) return "/api/video/:id";
        return req.path.split("?")[0];
    };

    const apiAnalytics = expressAnalytics(process.env.PRIVATE_API_ANALYTICS_KEY, apiAnalyticsConfig);

    const customMiddleware = (req, res, next) => {
        if (req.path.startsWith("/api/")) {
            return apiAnalytics(req, res, next);
        }
        next();
    };

    app.use(customMiddleware);
}

app.use(morgan("[:date[iso]] :remote-addr :method :url HTTP/:http-version :status :res[content-length] - :response-time ms"));

app.use(handler);

app.listen(3000, () => {
    console.log("listening on port 3000");
});
