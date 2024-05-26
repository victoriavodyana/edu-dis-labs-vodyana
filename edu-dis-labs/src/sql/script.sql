-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Account` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` CHAR(255) NOT NULL,
  `password` CHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Survey`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Survey` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `isPaused` TINYINT UNSIGNED NOT NULL,
  `isNamed` TINYINT UNSIGNED NOT NULL,
  `name` CHAR(255) NULL,
  `duration` CHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_Survey_Account1`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`Account` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Question`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Question` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Text` CHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_Question_Survey1`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`Survey` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Response`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Response` (
  `id` INT UNSIGNED NULL AUTO_INCREMENT,
  `Value` VARCHAR(16384) NULL,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_Response_Question`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`Question` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Response_Account1`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`Account` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Link`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Link` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `uses` INT NOT NULL,
  `responces` INT NOT NULL,
  `usageLimit` INT NULL,
  `responceLimit` INT NULL,
  `path` CHAR(32) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_Link_Survey1`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`Survey` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
