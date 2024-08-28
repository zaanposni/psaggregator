import { env } from "$env/dynamic/public";
import { writable } from "svelte/store";

export const MAIL_TO_URL = "mailto:psaggregator@zaanposni.com";
export const LEGAL_URL = env.PUBLIC_LEGAL_URL;
export const MICROANALYTICS_ID = env.PUBLIC_MICROANALYTICS_ID;
export const KOFI_USERNAME = env.PUBLIC_KOFI_USERNAME;

export const GITHUB_URL = "https://github.com/zaanposni/psaggregator";
export const GITHUB_AUTHOR_URL = "https://github.com/zaanposni";

export const SHOW_ABSOLUTE_DATES = writable(false);
export const VIDEO_COMPLEXE_VIEW = writable(false);
export const LINK_YOUTUBE = writable(false);

export const SHOW_ABSOLUTE_DATES_KEY = "showAbsoluteDates";
export const VIDEO_COMPLEXE_VIEW_KEY = "videoComplexeView";
export const LINK_YOUTUBE_KEY = "linkYoutube";
