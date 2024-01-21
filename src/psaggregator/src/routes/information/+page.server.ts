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

    return {
        youtubeCommunityPosts
    };
}
