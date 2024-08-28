import { json } from "@sveltejs/kit";
import prisma from "$lib/prisma";

export async function GET({ url }) {
    let skip = 0;
    const skipParam = url.searchParams.get("skip");
    if (skipParam) {
        try {
            skip = parseInt(skipParam);
        } finally {
            if (!skip) skip = 0;
        }
    }

    const data = await prisma.contentPiece.findMany({
        select: {
            id: true,
            title: true,
            href: true,
            secondaryHref: true,
            imageUri: true,
            startDate: true,
            duration: true,
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
        take: 50,
        skip
    });

    return json(data);
}
