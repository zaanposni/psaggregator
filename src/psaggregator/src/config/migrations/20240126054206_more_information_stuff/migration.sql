-- AlterTable
ALTER TABLE `Information` ADD COLUMN `additionalInfo` VARCHAR(1024) NULL;

-- CreateTable
CREATE TABLE `InformationResource` (
    `id` VARCHAR(191) NOT NULL,
    `remoteId` VARCHAR(191) NULL,
    `informationId` VARCHAR(191) NOT NULL,
    `imageUri` VARCHAR(1024) NULL,
    `videoUri` VARCHAR(1024) NULL,
    `importedAt` DATETIME(3) NOT NULL,
    `importedFrom` ENUM('Unknown', 'PietSmietDE', 'Instagram', 'Twitter', 'Threads', 'Reddit', 'YouTube', 'OpenAI', 'Custom') NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `InformationResource` ADD CONSTRAINT `InformationResource_informationId_fkey` FOREIGN KEY (`informationId`) REFERENCES `Information`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
