Create Table `shared_expenses`.`expenses` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `person` VARCHAR(255) NOT NULL,
    `amount` INT NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;