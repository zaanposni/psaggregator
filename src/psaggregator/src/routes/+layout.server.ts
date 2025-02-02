import prisma from "$lib/prisma";
import type { Announcement } from "@prisma/client";

export async function load() {
    const announcements = (await prisma.announcement.findMany()) as Announcement[];
    const twitchStatus = await prisma.twitchStatus.findFirst();

    return {
        announcements,
        twitchStatus
    };
}
