import prisma from "$lib/prisma";
import moment from "moment";

export async function load() {
    const upperBound = moment().endOf("day").toDate();
    const lowerBound = moment().startOf("day").toDate();

    const lowerBoundYoutubeStreamplan = moment().startOf("day").subtract(1, "week").toDate();

    const [today, videos, upcomingStreams, redditPosts, youtubeCommunityPosts, instagramPosts, twitterPosts, youtubeStreamplanPost] =
        await Promise.all([
            prisma.scheduledContentPiece.findMany({
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
            }),
            // ===
            prisma.contentPiece.findMany({
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
            }),
            // ===
            prisma.scheduledContentPiece.findMany({
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
                take: 8
            }),
            // ===
            prisma.redditPost.findMany({
                orderBy: {
                    sticky: "desc"
                },
                take: 10
            }),
            // ===
            prisma.information.findMany({
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
                take: 5
            }),
            // ===
            prisma.information.findMany({
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
                    InformationResource: true
                },
                orderBy: {
                    date: "desc"
                },
                take: 3
            }),
            // ===
            prisma.information.findMany({
                where: {
                    importedFrom: {
                        equals: "Twitter"
                    },
                    href: {
                        not: null
                    },
                    date: {
                        not: null
                    }
                },
                include: {
                    InformationResource: true
                },
                orderBy: {
                    date: "desc"
                },
                take: 7
            }),
            // ===
            prisma.information.findFirst({
                where: {
                    importedFrom: {
                        equals: "YouTube"
                    },
                    href: {
                        not: null
                    },
                    text: {
                        contains: "stream"
                    },
                    date: {
                        not: null,
                        gt: lowerBoundYoutubeStreamplan
                    }
                },
                orderBy: {
                    date: "desc"
                }
            })
        ]);

    return {
        today,
        videos,
        upcomingStreams,
        redditPosts,
        youtubeCommunityPosts,
        instagramPosts,
        twitterPosts,
        youtubeStreamplanPost
    };
}
