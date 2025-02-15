import { json } from "@sveltejs/kit";
import prisma from "$lib/prisma";

export async function GET() {
    const videoCount = await prisma.contentPiece.count({
        where: {
            type: {
                equals: "PSVideo"
            },
            imageUri: {
                not: null
            },
            href: {
                not: null
            },
            startDate: {
                not: null
            },
            OR: [
                {
                    href: {
                        contains: "youtu.be"
                    }
                },
                {
                    secondaryHref: {
                        contains: "youtu.be"
                    }
                }
            ]
        }
    });
    const skip = Math.floor(Math.random() * videoCount);
    const video = await prisma.contentPiece.findFirst({
        where: {
            type: {
                equals: "PSVideo"
            },
            imageUri: {
                not: null
            },
            href: {
                not: null
            },
            startDate: {
                not: null
            },
            OR: [
                {
                    href: {
                        contains: "youtu.be"
                    }
                },
                {
                    secondaryHref: {
                        contains: "youtu.be"
                    }
                }
            ]
        },
        orderBy: {
            startDate: "desc"
        },
        skip
    });

    return json(video);
}
