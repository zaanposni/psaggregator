-- CreateTable
CREATE TABLE `TwitchStatus` (
    `id` VARCHAR(191) NOT NULL,
    `title` VARCHAR(191) NOT NULL,
    `gameName` VARCHAR(191) NOT NULL,
    `viewers` INTEGER NOT NULL,
    `startedAt` DATETIME(3) NOT NULL,
    `live` BOOLEAN NOT NULL,
    `thumbnail` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
