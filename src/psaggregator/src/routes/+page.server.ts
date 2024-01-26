import prisma from "$lib/prisma";
import moment from "moment";

export async function load() {
    const upperBound = moment().endOf("day").toDate();
    const lowerBound = moment().startOf("day").toDate();

    const today = await prisma.scheduledContentPiece.findMany({
        where: {
            type: {
                equals: "PSVideo"
            },
            importedFrom: {
                equals: "PietSmietDE"
            },
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
                equals: "PSVideo"
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
        },
        take: 20
    });

    const upcomingStreams = await prisma.scheduledContentPiece.findMany({
        where: {
            type: {
                equals: "TwitchStream"
            },
            startDate: {
                gt: lowerBound
            }
        },
        orderBy: {
            startDate: "asc"
        },
        take: 5
    });

    const twitchStatus = await prisma.twitchStatus.findFirst();

    const redditPosts = await prisma.redditPost.findMany({
        orderBy: {
            sticky: "desc"
        },
        take: 10
    });

    const youtubeCommunityPosts = await prisma.information.findMany({
        where: {
            importedFrom: {
                equals: "YouTube"
            },
            href: {
                not: null
            },
            date: {
                not: null
            }
        },
        orderBy: {
            date: "desc"
        },
        take: 3
    });

    const instagramPosts = await prisma.information.findMany({
        where: {
            importedFrom: {
                equals: "Instagram"
            },
            href: {
                not: null
            },
            date: {
                not: null
            }
        },
        include: {
            InformationResource: true,
        },
        orderBy: {
            date: "desc"
        },
        take: 3
    });

    return {
        videos,
        upcomingStreams,
        youtubeCommunityPosts,
        instagramPosts,
        today,
        twitchStatus,
        redditPosts
    };
}
