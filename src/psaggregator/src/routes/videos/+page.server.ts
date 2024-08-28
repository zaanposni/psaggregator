import prisma from "$lib/prisma";

export async function load() {
    const videos = await prisma.contentPiece.findMany({
        select: {
            id: true,
            title: true,
            href: true,
            secondaryHref: true,
            imageUri: true,
            startDate: true,
            duration: true
        },
        where: {
            type: {
                equals: "PSVideo"
            },
            href: {
                not: null
            },
            imageUri: {
                not: null
            },
            startDate: {
                not: null
            }
        },
        orderBy: {
            startDate: "desc"
        },
        take: 50
    });

    return {
        videos
    };
}
