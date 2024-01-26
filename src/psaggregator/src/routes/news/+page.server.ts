import prisma from "$lib/prisma";

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
        take: 10
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
        take: 10
    });

    return {
        youtubeCommunityPosts,
        instagramPosts
    };
}
