import { createRequire as _createRequire } from 'module'
export const createCursedRequire: (path: string | URL) => <TShape>(id: string) => TShape = _createRequire

const require = createCursedRequire(import.meta.url ?? __filename)
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

export default prisma;
