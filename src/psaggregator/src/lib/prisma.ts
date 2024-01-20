import { createRequire } from "module"; // https://github.com/prisma/prisma/issues/15614
const require = createRequire(import.meta.url);
const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

export default prisma;
