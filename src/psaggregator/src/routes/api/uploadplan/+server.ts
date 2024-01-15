import { json } from "@sveltejs/kit";
import prisma from "$lib/prisma";
import moment from "moment";

export async function GET({ url }) {
    let now = moment();
    if (url.searchParams.has("date")) {
        try {
            now = moment(url.searchParams.get("date"));
        } finally {
            if (!now || !now.isValid()) {
                now = moment();
            }
        }
    }

    const upperBound = now.clone().endOf("day").toDate();
    const lowerBound = now.clone().startOf("day").toDate();

    const data = await prisma.contentPiece.findMany({
        where: {
            startDate: {
                lt: upperBound,
                gt: lowerBound
            }
        },
        orderBy: {
            startDate: "asc"
        }
    });

    return json(data);
}
