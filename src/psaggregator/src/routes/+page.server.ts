import prisma from "$lib/prisma";
import moment from "moment";

export async function load() {
    const upperBound = moment().endOf("day").toDate();
    const lowerBound = moment().startOf("day").toDate();

    let today = await prisma.contentPiece.findMany({
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

    today = today.filter((contentPiece) => moment().isSame(contentPiece.startDate, "day"));

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
