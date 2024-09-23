import prisma from "$lib/prisma";
import moment from "moment";
import type { Information, InformationResource } from "@prisma/client";

export async function load() {
    const oneDayAgo = moment().subtract(1, "day").toDate();

    const [youtubeCommunityPosts, instagramPosts, instagramStories, twitterPosts]: Array<
        Array<Information & { InformationResource: InformationResource[] }>
    > = await Promise.all([
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
            take: 20
        }),
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
            take: 20
        }),
        prisma.information.findMany({
            where: {
                importedFrom: {
                    equals: "InstagramStory"
                },
                href: {
                    not: null
                },
                date: {
                    not: null,
                    gte: oneDayAgo
                }
            },
            include: {
                InformationResource: true
            },
            orderBy: {
                date: "asc"
            }
        }),
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
            take: 20
        })
    ]);

    return {
        youtubeCommunityPosts,
        instagramPosts,
        instagramStories,
        twitterPosts
    };
}
