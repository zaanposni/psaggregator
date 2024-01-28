import prisma from "$lib/prisma";
import type { Announcement } from "@prisma/client";

export async function load() {
    const announcements = await prisma.announcement.findMany() as Announcement[];

    return {
        announcements
    };
}
