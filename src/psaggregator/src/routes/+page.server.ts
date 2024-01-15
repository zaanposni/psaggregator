import prisma from "$lib/prisma";
import moment from "moment";

export async function load() {
    const upperBound = moment().endOf("day").toDate();
    const lowerBound = moment().startOf("day").toDate();

    const today = await prisma.contentPiece.findMany({
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

    const videos = await prisma.contentPiece.findMany({
        where: {
            type: {
                equals: "Video"
            },
            href: {
                not: null
            },
            startDate: {
                not: null
            }
        },
        orderBy: {
            startDate: "desc"
        }
    });

    const twitchStatus = await prisma.twitchStatus.findFirst();

    return {
        videos,
        today,
        twitchStatus
    };
}
