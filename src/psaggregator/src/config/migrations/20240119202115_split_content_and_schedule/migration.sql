/*
  Warnings:

  - The values [Video] on the enum `ContentPiece_type` will be removed. If these variants are still used in the database, this will fail.
  - Made the column `remoteId` on table `ContentPiece` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE `ContentPiece` MODIFY `type` ENUM('Unknown', 'PSVideo', 'TwitchStream') NOT NULL,
    MODIFY `remoteId` VARCHAR(191) NOT NULL;

-- CreateTable
CREATE TABLE `ScheduledContentPiece` (
    `id` VARCHAR(191) NOT NULL,
    `remoteId` VARCHAR(191) NULL,
    `title` VARCHAR(191) NOT NULL,
    `description` VARCHAR(191) NULL,
    `additionalInfo` VARCHAR(191) NULL,
    `startDate` DATETIME(3) NULL,
    `imageUri` VARCHAR(191) NULL,
    `href` VARCHAR(191) NULL,
    `secondaryHref` VARCHAR(191) NULL,
    `duration` INTEGER NULL,
    `importedAt` DATETIME(3) NOT NULL,
    `importedFrom` ENUM('Unknown', 'PietSmietDE', 'Instagram', 'Twitter', 'Threads', 'Reddit', 'Custom') NOT NULL,
    `type` ENUM('Unknown', 'PSVideo', 'TwitchStream') NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
