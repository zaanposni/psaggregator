-- AlterTable
ALTER TABLE `ContentPiece` MODIFY `importedFrom` ENUM('Unknown', 'PietSmietDE', 'Instagram', 'Twitter', 'Threads', 'Reddit', 'YouTube', 'OpenAI', 'Custom') NOT NULL;

-- AlterTable
ALTER TABLE `Information` MODIFY `importedFrom` ENUM('Unknown', 'PietSmietDE', 'Instagram', 'Twitter', 'Threads', 'Reddit', 'YouTube', 'OpenAI', 'Custom') NOT NULL;

-- AlterTable
ALTER TABLE `ScheduledContentPiece` MODIFY `importedFrom` ENUM('Unknown', 'PietSmietDE', 'Instagram', 'Twitter', 'Threads', 'Reddit', 'YouTube', 'OpenAI', 'Custom') NOT NULL;
