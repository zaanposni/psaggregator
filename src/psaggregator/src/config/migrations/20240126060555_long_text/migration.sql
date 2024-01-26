-- AlterTable
ALTER TABLE `ContentPiece` MODIFY `title` LONGTEXT NOT NULL,
    MODIFY `description` LONGTEXT NULL,
    MODIFY `additionalInfo` LONGTEXT NULL;

-- AlterTable
ALTER TABLE `Information` MODIFY `text` LONGTEXT NOT NULL,
    MODIFY `additionalInfo` LONGTEXT NULL;

-- AlterTable
ALTER TABLE `RedditPost` MODIFY `title` LONGTEXT NOT NULL,
    MODIFY `description` LONGTEXT NULL;

-- AlterTable
ALTER TABLE `ScheduledContentPiece` MODIFY `title` LONGTEXT NOT NULL,
    MODIFY `description` LONGTEXT NULL,
    MODIFY `additionalInfo` LONGTEXT NULL;
