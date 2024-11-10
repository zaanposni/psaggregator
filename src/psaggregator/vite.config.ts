import { sentrySvelteKit } from "@sentry/sveltekit";
import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

import { readFileSync } from "fs";
import { fileURLToPath } from "url";

const file = fileURLToPath(new URL("package.json", import.meta.url));
const json = readFileSync(file, "utf8");
const pkg = JSON.parse(json);

export default defineConfig({
    build: {
        sourcemap: process.env.SENTRY_UPLOAD_SOURCEMAPS === "true"
    },
    plugins: [
        sentrySvelteKit({
            sourceMapsUploadOptions:
                process.env.SENTRY_UPLOAD_SOURCEMAPS === "true"
                    ? {
                          release: {
                              name: pkg.version
                          },
                          org: process.env.SENTRY_ORG,
                          project: process.env.SENTRY_PROJECT,
                          authToken: process.env.SENTRY_AUTH_TOKEN
                      }
                    : undefined
        }),
        sveltekit()
    ]
});
