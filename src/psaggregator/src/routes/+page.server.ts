import prisma from "$lib/prisma";
import moment from "moment";

export async function load() {
    const upperBound = moment().add(4, "week").toDate();
    const lowerBound = moment().subtract(1, "week").toDate();

    const contentPieces = await prisma.contentPiece.findMany({
        where: {
            startDate: {
                lt: upperBound,
                gt: lowerBound
            }
        },
        orderBy: {
            startDate: "asc"
        }
    });

    const today = contentPieces.filter((contentPiece) =>
        moment().isSame(contentPiece.startDate, "day")
    );

    return {
        contentPieces,
        today
    };
}
