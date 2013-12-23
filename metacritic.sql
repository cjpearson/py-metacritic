DROP TABLE IF EXISTS `movies`;
CREATE TABLE `movies` (
        title varchar(200) default null,
        movie_url varchar(200) not null,
        uScore int default null,
        cScore int default null,
        release_date DATE default null,
        movie_id int not null auto_increment primary key

) ENGINE=InnoDB;

DROP TABLE IF EXISTS `critics`;
CREATE TABLE `critics` (
        name varchar(100) default null,
        publication varchar(100) default null,
        critic_id int not null auto_increment primary key
        
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `reviews`;
CREATE TABLE `reviews` (
        movie_url varchar(200) default null,
        critic_id int default null,
        movie_id int default null,
        score int default null,
        description varchar(1000) default null,
        review_id int not null auto_increment primary key
        
) Engine=InnoDB;