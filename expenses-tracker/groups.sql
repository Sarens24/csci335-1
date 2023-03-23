Create Table `shared_expenses`.`groups` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `person1` VARCHAR(255) NOT NULL,
    `person2` VARCHAR(255) NOT NULL,
    `person3` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;