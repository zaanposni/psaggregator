import * as Sentry from "@sentry/sveltekit";
import { version } from "$app/environment";
import { SENTRY_DSN } from "./config/config";

if (SENTRY_DSN) {
    Sentry.init({
        dsn: SENTRY_DSN,

        environment: import.meta.env.MODE,
        release: version,

        tracesSampleRate: 1
    });
}

export const handleError = Sentry.handleErrorWithSentry();
