import { json } from "@sveltejs/kit";
import prisma from "$lib/prisma";
import moment from "moment";

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

    let newSince = undefined;
    if (url.searchParams.has("newSince")) {
        const value = url.searchParams.get("newSince");
        if (value) {
            try {
                newSince = moment.unix(parseInt(value));
            } finally {
                if (!newSince || !newSince.isValid()) {
                    newSince = undefined;
                }
            }
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
                not: null,
                gt: newSince ? newSince.toDate() : undefined
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
