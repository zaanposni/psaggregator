/*
  Warnings:

  - Added the required column `comments` to the `RedditPost` table without a default value. This is not possible if the table is not empty.
  - Added the required column `sticky` to the `RedditPost` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE `RedditPost` ADD COLUMN `comments` INTEGER NOT NULL,
    ADD COLUMN `sticky` BOOLEAN NOT NULL;
