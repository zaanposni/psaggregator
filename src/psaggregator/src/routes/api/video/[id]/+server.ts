import { json } from "@sveltejs/kit";
import prisma from "$lib/prisma";

export async function GET({ params }) {
    const data = await prisma.contentPiece.findFirst({
        where: {
            AND: {
                type: "PSVideo",
                importedFrom: "PietSmietDE"
            },
            OR: [{ id: params.id }, { remoteId: params.id }, { href: params.id }, { secondaryHref: params.id }]
        }
    });

    return json(data);
}
