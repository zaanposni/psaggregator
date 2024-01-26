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

    const type = url.searchParams.get("type") ?? undefined;

    let date = null;
    if (url.searchParams.has("date")) {
        try {
            date = moment(url.searchParams.get("date"));
        } finally {
            if (!date || !date.isValid()) {
                date = null;
            }
        }
    }

    let data = [];

    if (date) {
        const upperBound = date.clone().endOf("day").toDate();
        const lowerBound = date.clone().startOf("day").toDate();

        data = await prisma.information.findMany({
            where: {
                date: {
                    lt: upperBound,
                    gt: lowerBound
                },
                importedFrom: type,
            },
            include: {
                InformationResource: true,
            },
            orderBy: {
                date: "desc"
            },
            skip,
            take: 20,
        });
    } else {
        data = await prisma.information.findMany({
            where: {
                importedFrom: type,
            },
            include: {
                InformationResource: true,
            },
            orderBy: {
                date: "desc"
            },
            skip,
            take: 20
        });
    }

    return json(data);
}
