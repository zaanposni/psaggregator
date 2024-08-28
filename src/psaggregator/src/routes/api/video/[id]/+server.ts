import { json } from "@sveltejs/kit";
import prisma from "$lib/prisma";

export async function GET({ params }) {
    const data = await prisma.contentPiece.findFirst({
        where: {
            type: "PSVideo",
            importedFrom: "PietSmietDE",
            id: params.id
        }
    });

    return json(data);
}
