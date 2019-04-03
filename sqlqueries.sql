CREATE TABLE `scraperDB`.`SearchQueries` (
    `id` INT NOT NULL AUTO_INCREMENT ,
    `arg` VARCHAR(255) CHARACTER SET hp8 COLLATE hp8_english_ci NOT NULL ,
    PRIMARY KEY (`id`)
    ) ENGINE = InnoDB COMMENT = 'table for queries passed in q';


CREATE TABLE `scraperDB`.`ScrapedData` (
    `id` INT NOT NULL AUTO_INCREMENT ,
    `qusRef` INT NOT NULL ,
    `questionHeading` VARCHAR(255) NOT NULL ,
    `questionLink` VARCHAR(255) NOT NULL ,
    `questionAnswer` TEXT NOT NULL ,
    PRIMARY KEY  (`id`)
    ) ENGINE = InnoDB;
