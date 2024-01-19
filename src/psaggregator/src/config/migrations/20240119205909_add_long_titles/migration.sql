-- AlterTable
ALTER TABLE `ContentPiece` MODIFY `title` VARCHAR(1024) NOT NULL,
    MODIFY `description` VARCHAR(1024) NULL,
    MODIFY `additionalInfo` VARCHAR(1024) NULL,
    MODIFY `imageUri` VARCHAR(1024) NULL,
    MODIFY `href` VARCHAR(1024) NULL,
    MODIFY `secondaryHref` VARCHAR(1024) NULL;

-- AlterTable
ALTER TABLE `Information` MODIFY `text` VARCHAR(1024) NOT NULL,
    MODIFY `imageUri` VARCHAR(1024) NULL,
    MODIFY `href` VARCHAR(1024) NULL;

-- AlterTable
ALTER TABLE `RedditPost` MODIFY `title` VARCHAR(1024) NOT NULL,
    MODIFY `description` VARCHAR(1024) NULL,
    MODIFY `imageUri` VARCHAR(1024) NULL,
    MODIFY `href` VARCHAR(1024) NULL;

-- AlterTable
ALTER TABLE `ScheduledContentPiece` MODIFY `title` VARCHAR(1024) NOT NULL,
    MODIFY `description` VARCHAR(1024) NULL,
    MODIFY `additionalInfo` VARCHAR(1024) NULL,
    MODIFY `imageUri` VARCHAR(1024) NULL,
    MODIFY `href` VARCHAR(1024) NULL,
    MODIFY `secondaryHref` VARCHAR(1024) NULL;

-- AlterTable
ALTER TABLE `TwitchStatus` MODIFY `title` VARCHAR(1024) NOT NULL,
    MODIFY `thumbnail` VARCHAR(1024) NOT NULL;
