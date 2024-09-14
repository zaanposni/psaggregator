import { json } from "@sveltejs/kit";
import prisma from "$lib/prisma";

export async function GET() {
    const videoCount = await prisma.contentPiece.count();
    const skip = Math.floor(Math.random() * videoCount);
    const video = await prisma.contentPiece.findFirst({
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
    });

    return json(video);
}
