/*
  Warnings:

  - Added the required column `upvotes` to the `RedditPost` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE `RedditPost` ADD COLUMN `upvotes` INTEGER NOT NULL;
