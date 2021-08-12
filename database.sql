CREATE TABLE `user`
(
    `id`         int AUTO_INCREMENT NOT NULL,
    `username`   varchar(50) UNIQUE NOT NULL,
    `password`   char(60)           NOT NULL,
    `created_at` timestamp DEFAULT NOW(),
    `updated_at` timestamp DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`id`)
);

CREATE TABLE `category`
(
    `id`         int AUTO_INCREMENT NOT NULL,
    `name`       varchar(50) UNIQUE NOT NULL,
    `created_at` timestamp DEFAULT NOW(),
    `updated_at` timestamp DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`id`)
);

CREATE TABLE `item`
(
    `id`          int AUTO_INCREMENT NOT NULL,
    `name`        varchar(200)  NOT NULL,
    `description` varchar(2000) NOT NULL,
    `user_id`     int           NOT NULL,
    `category_id` int           NOT NULL,
    `created_at`  timestamp DEFAULT NOW(),
    `updated_at`  timestamp DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
    FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
);

INSERT INTO `category` (`name`)
VALUES ('random'),
       ('nature'),
       ('music'),
       ('game'),
       ('people'),
       ('words'),
       ('sport'),
       ('technology'),
       ('entertainment'),
       ('date and times')