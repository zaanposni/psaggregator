-- CreateTable
CREATE TABLE `RedditPost` (
    `id` VARCHAR(191) NOT NULL,
    `title` VARCHAR(191) NOT NULL,
    `description` VARCHAR(191) NULL,
    `username` VARCHAR(191) NOT NULL,
    `publishedAt` DATETIME(3) NOT NULL,
    `imageUri` VARCHAR(191) NULL,
    `href` VARCHAR(191) NULL,
    `importedAt` DATETIME(3) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
