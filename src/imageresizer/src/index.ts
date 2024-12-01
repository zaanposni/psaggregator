import express, { Request, Response } from "express";
import sharp from "sharp";
import fs from "fs";
import path from "path";
import morgan from "morgan";
import winston from "winston";

const logger = winston.createLogger({
    level: "info",
    format: winston.format.combine(winston.format.timestamp(), winston.format.cli()),
    transports: [new winston.transports.Console()],
});

const app = express();
const port = process.env.PORT || 3000;
const cdnFiles = process.env.CDN_FILE_BASE_DIRECTORY || "/app/cdn";

app.get("/_health", (_, res) => {
    res.send("OK");
});

app.get("/cdn/:dir/:filename", async (req: Request<{ dir: string; filename: string }>, res: Response) => {
    let { dir, filename } = req.params;
    const { width } = req.query;

    if (!filename) {
        logger.error("Missing filename parameter");
        res.status(400).send("Missing filename parameter");
        return;
    }

    filename = path.join(dir, filename).replace(/\.\./g, "").replace(/^\//g, "");

    if (filename.endsWith(".mp4")) {
        const filePath = path.join(cdnFiles, filename);
        logger.info(`Serving video: "${filename}"`);

        if (!fs.existsSync(filePath)) {
            logger.error(`Resource not found: "${filePath}"`);
            res.status(404).send("Resource not found");
            return;
        }

        res.contentType("video/mp4");
        return res.sendFile(filePath);
    }

    // Validate parameters
    const validWidths = ["300", "768", "original"];

    if (width && !validWidths.includes(width.toString())) {
        logger.error(`Invalid width parameter: "${width}"`);
        res.status(400).send("Invalid width parameter, must be one of: 300, 768, original");
        return;
    }

    const targetWidth = width ? (width === "original" ? undefined : parseInt(width.toString())) : undefined;

    // convert image to specified format and size
    const originalFilePath = path.join(cdnFiles, filename);
    const specificFileName = targetWidth === undefined ? filename : `${filename.split(".")[0]}-w${targetWidth}.jpg`;
    const specificFilePath = path.join(cdnFiles, specificFileName);
    logger.info(`Serving image: "${specificFilePath}"`);

    if (!fs.existsSync(specificFilePath)) {
        if (specificFileName === filename && !fs.existsSync(originalFilePath)) {
            logger.error(`Original Resource not found: "${originalFilePath}"`);
            res.status(404).send("Resource not found");
            return;
        }

        logger.info(`Generating image: "${specificFilePath}" from "${originalFilePath}"`);

        try {
            const image = sharp(originalFilePath);
            if (targetWidth) {
                image.resize(targetWidth);
            }

            image.toFormat("jpg", { quality: 100 });

            await image.toFile(specificFilePath);
        } catch (error) {
            logger.error(`Failed to generate image: "${specificFilePath}"`, error);
            res.status(500).send("Failed to generate image");
            return;
        }
    }

    res.contentType(`image/jpg`);
    res.sendFile(specificFilePath);
});

app.use(
    morgan("[:date[iso]] :remote-addr :method :url HTTP/:http-version :status :res[content-length] - :response-time ms")
);

app.listen(port, () => {
    console.log(`[server]: Server is running at http://localhost:${port}`);
});
