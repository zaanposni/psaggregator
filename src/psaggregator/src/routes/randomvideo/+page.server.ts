import prisma from "$lib/prisma";
import type { ContentPiece } from "@prisma/client";

export async function load(e) {
    e.depends("data:randomvideo");

    const videoCount = await prisma.contentPiece.count();
    const skip = Math.floor(Math.random() * videoCount);
    const video = (await prisma.contentPiece.findFirst({
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
        skip
    })) as ContentPiece;

    return {
        video
    };
}
