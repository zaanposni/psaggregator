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
        where: {
            type: "PSVideo",
            importedFrom: "PietSmietDE"
        },
        orderBy: {
            startDate: "desc"
        },
        skip,
        take: 20
    });

    return json(data);
}
