-- AlterTable
ALTER TABLE `ContentPiece` ADD COLUMN `remoteId` VARCHAR(191) NULL,
    ADD COLUMN `secondaryHref` VARCHAR(191) NULL;

-- AlterTable
ALTER TABLE `Information` ADD COLUMN `remoteId` VARCHAR(191) NULL;
