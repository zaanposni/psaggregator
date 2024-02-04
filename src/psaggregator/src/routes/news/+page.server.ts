import prisma from "$lib/prisma";
import moment from "moment";
import type { Information, InformationResource } from "@prisma/client";


export async function load() {
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
        take: 20
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
        take: 20
    });

    const oneDayAgo = moment().subtract(1, "day").toDate();
    const instagramStories = await prisma.information.findMany({
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
            InformationResource: true,
        },
        orderBy: {
            date: "desc"
        }
    }) as Array<Information & { InformationResource: InformationResource[] }>;

    return {
        youtubeCommunityPosts,
        instagramPosts,
        instagramStories
    };
}
