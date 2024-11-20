import { handleErrorWithSentry, replayIntegration } from "@sentry/sveltekit";
import * as Sentry from "@sentry/sveltekit";
import { version } from "$app/environment";
import { SENTRY_DSN } from "./config/config";

if (SENTRY_DSN) {
    Sentry.init({
        dsn: SENTRY_DSN,

        environment: import.meta.env.MODE,
        release: version,

        tracesSampleRate: 1.0,
        replaysSessionSampleRate: import.meta.env.MODE === "development" ? 0 : 0.1,
        replaysOnErrorSampleRate: 1.0,

        integrations: [
            replayIntegration({
                maskAllInputs: false,
                maskAllText: false,
                blockAllMedia: false
            })
        ]
    });
}

export const handleError = handleErrorWithSentry();
