-- CreateTable
CREATE TABLE `ContentPiece` (
    `id` VARCHAR(191) NOT NULL,
    `title` VARCHAR(191) NOT NULL,
    `description` VARCHAR(191) NULL,
    `additionalInfo` VARCHAR(191) NULL,
    `startDate` DATETIME(3) NULL,
    `imageUri` VARCHAR(191) NULL,
    `href` VARCHAR(191) NULL,
    `importedAt` DATETIME(3) NOT NULL,
    `importedFrom` ENUM('Unknown', 'PietSmietDE', 'Instagram', 'Twitter', 'Threads', 'Reddit', 'Custom') NOT NULL,
    `type` ENUM('Unknown', 'Video', 'TwitchStream') NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Information` (
    `id` VARCHAR(191) NOT NULL,
    `text` VARCHAR(191) NOT NULL,
    `imageUri` VARCHAR(191) NULL,
    `href` VARCHAR(191) NULL,
    `date` DATETIME(3) NULL,
    `importedAt` DATETIME(3) NOT NULL,
    `importedFrom` ENUM('Unknown', 'PietSmietDE', 'Instagram', 'Twitter', 'Threads', 'Reddit', 'Custom') NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
