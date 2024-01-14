/** @type {import('tailwindcss').Config}*/

const forms = require("@tailwindcss/forms");
const skeleton = require("@skeletonlabs/tw-plugin").skeleton;
const join = require("path").join;
const dirname = require("path").dirname;

const modulePath = require.resolve("@skeletonlabs/skeleton");
const rootPath = dirname(modulePath);

const config = {
    content: [join("./src/**/*.{html,js,svelte,ts}"), join(rootPath, "**/*.{html,js,svelte,ts}")],

    theme: {
        extend: {}
    },

    plugins: [
        forms,
        skeleton({
            themes: { preset: ["rocket"] }
        })
    ],

    darkMode: "class"
};

module.exports = config;