CREATE TABLE `Artists` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	`birthday` DATE NOT NULL,
	`date_of_death` DATE NOT NULL,
	`nationality` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Paintings` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	`creating_date` DATE NOT NULL,
	`cost_$m` float NOT NULL,
	`technics_id` int NOT NULL,
	`painting_styles_id` int NOT NULL,
	`periods_id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Technics` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Painting styles` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Historical periods` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	`begin_date` DATE NOT NULL,
	`ending_date` DATE NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Painting by artists` (
	`artist_id` int NOT NULL,
	`painting_id` int NOT NULL
);

CREATE TABLE `Subtechnics` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Tech by subtech` (
	`tech_id` int NOT NULL,
	`subtech_id` int NOT NULL
);

ALTER TABLE `Paintings` ADD CONSTRAINT `Paintings_fk0` FOREIGN KEY (`technics_id`) REFERENCES `Technics`(`id`);

ALTER TABLE `Paintings` ADD CONSTRAINT `Paintings_fk1` FOREIGN KEY (`painting_styles_id`) REFERENCES `Painting styles`(`id`);

ALTER TABLE `Paintings` ADD CONSTRAINT `Paintings_fk2` FOREIGN KEY (`periods_id`) REFERENCES `Historical periods`(`id`);

ALTER TABLE `Painting by artists` ADD CONSTRAINT `Painting by artists_fk0` FOREIGN KEY (`artist_id`) REFERENCES `Artists`(`id`);

ALTER TABLE `Painting by artists` ADD CONSTRAINT `Painting by artists_fk1` FOREIGN KEY (`painting_id`) REFERENCES `Paintings`(`id`);

ALTER TABLE `Tech by subtech` ADD CONSTRAINT `Tech by subtech_fk0` FOREIGN KEY (`tech_id`) REFERENCES `Subtechnics`(`id`);

ALTER TABLE `Tech by subtech` ADD CONSTRAINT `Tech by subtech_fk1` FOREIGN KEY (`subtech_id`) REFERENCES `Technics`(`id`);
