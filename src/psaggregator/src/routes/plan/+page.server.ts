import prisma from "$lib/prisma";
import type { ScheduledContentPiece } from "@prisma/client";
import moment from "moment";

export async function load() {
    const upperBound = moment().endOf("day").toDate();
    const lowerBound = moment().startOf("day").toDate();

    const today = (await prisma.scheduledContentPiece.findMany({
        where: {
            type: {
                equals: "PSVideo"
            },
            importedFrom: {
                equals: "PietSmietDE"
            },
            startDate: {
                lt: upperBound,
                gt: lowerBound
            }
        },
        orderBy: {
            startDate: "asc"
        }
    })) as ScheduledContentPiece[];

    return {
        today
    };
}
