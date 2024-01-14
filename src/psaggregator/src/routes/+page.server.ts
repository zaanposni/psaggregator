import { PrismaClient } from '@prisma/client'
import moment from 'moment';

export async function load() {
    const prisma = new PrismaClient();
    const upperBound = moment().add(4, 'week').toDate();
    const lowerBound = moment().subtract(1, 'week').toDate();

	return {
		contentPieces: await prisma.contentPiece.findMany({
            where: {
                importedAt: {
                    lt: upperBound,
                    gt: lowerBound,
                },
            },
        }),
	};
}