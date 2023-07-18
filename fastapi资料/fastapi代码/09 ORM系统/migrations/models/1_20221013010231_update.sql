-- upgrade --
ALTER TABLE `course` ADD `addr` VARCHAR(32) NOT NULL  COMMENT '教室' DEFAULT '';
-- downgrade --
ALTER TABLE `course` DROP COLUMN `addr`;
