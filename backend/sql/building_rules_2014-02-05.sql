# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.35-0ubuntu0.12.04.2)
# Database: building_rules
# Generation Time: 2014-02-05 22:56:21 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table actions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `actions`;

CREATE TABLE `actions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(11) DEFAULT NULL,
  `action_name` varchar(16) DEFAULT NULL,
  `rule_consequent` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `actions` WRITE;
/*!40000 ALTER TABLE `actions` DISABLE KEYS */;

INSERT INTO `actions` (`id`, `category`, `action_name`, `rule_consequent`, `description`)
VALUES
	(1,'LIGHT','LIGHT_ON','turn on the light','turn on the light'),
	(2,'LIGHT','LIGHT_OFF','turn off the light','turn off the light'),
	(3,'HEATING','HEATING_ON','turn on the heating','turn on the heating'),
	(4,'HEATING','HEATING_OFF','turn off the heating','turn off the heating'),
	(5,'COOLING','COOLING_ON','turn on the cooling','turn off the cooling'),
	(6,'COOLING','COOLING_OFF','turn off the cooling','turn off the cooling'),
	(7,'WINDOWS','WINDOWS_OPEN','open the windows','open the windows'),
	(8,'WINDOWS','WINDOWS_CLOSE','close the windows','close the windows'),
	(9,'CURTAINS','CURTAINS_OPEN','open the curtains','open the curtains'),
	(10,'CURTAINS','CURTAINS_CLOSE','close the curtains','close the curtains');

/*!40000 ALTER TABLE `actions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table buildings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `buildings`;

CREATE TABLE `buildings` (
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `label` varchar(11) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`building_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `buildings` WRITE;
/*!40000 ALTER TABLE `buildings` DISABLE KEYS */;

INSERT INTO `buildings` (`building_name`, `label`, `description`)
VALUES
	('CSE','CSE','Computer Science Eng');

/*!40000 ALTER TABLE `buildings` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `groups`;

CREATE TABLE `groups` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `description` longtext,
  `cross_rooms_validation` int(11) DEFAULT NULL,
  `cross_rooms_validation_categories` varchar(1024) DEFAULT '',
  PRIMARY KEY (`id`,`building_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;

INSERT INTO `groups` (`id`, `building_name`, `description`, `cross_rooms_validation`, `cross_rooms_validation_categories`)
VALUES
	(1,'CSE','WeekendManager',0,'[]'),
	(2,'CSE','DefaultRules',0,'[]');

/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table notifications
# ------------------------------------------------------------

DROP TABLE IF EXISTS `notifications`;

CREATE TABLE `notifications` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `send_timestamp` timestamp NULL DEFAULT NULL,
  `message_subject` varchar(128) DEFAULT NULL,
  `message_text` longtext,
  `recipient_uuid` int(11) DEFAULT NULL,
  `message_read` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;

INSERT INTO `notifications` (`id`, `send_timestamp`, `message_subject`, `message_text`, `recipient_uuid`, `message_read`)
VALUES
	(1,'2014-02-05 14:46:46','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then turn off the light>>. The new rule is << if today is Sunday then turn off the light >>',1,1),
	(2,'2014-02-05 14:46:46','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then turn off the light>>. The new rule is << if today is Sunday then turn off the light >>',3,0),
	(3,'2014-02-05 14:47:39','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then turn on the heating>>. The new rule is << if today is Sunday then turn on the heating >>',1,1),
	(4,'2014-02-05 14:47:39','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then turn on the heating>>. The new rule is << if today is Sunday then turn on the heating >>',3,0),
	(5,'2014-02-05 14:47:46','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then close the windows>>. The new rule is << if today is Sunday then close the windows >>',1,1),
	(6,'2014-02-05 14:47:46','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then close the windows>>. The new rule is << if today is Sunday then close the windows >>',3,0),
	(7,'2014-02-05 14:47:50','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then turn off the cooling>>. The new rule is << if today is Sunday then turn off the cooling >>',1,1),
	(8,'2014-02-05 14:47:50','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if today is Sunday then turn off the cooling>>. The new rule is << if today is Sunday then turn off the cooling >>',3,0),
	(9,'2014-02-05 14:48:02','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if it is rainy then close the windows>>. The new rule is << if it is rainy then close the windows >>',1,1),
	(10,'2014-02-05 14:48:02','Rule modified in building CSE room 2142','The user anacci edited (or tried to edit) the rule <<if it is rainy then close the windows>>. The new rule is << if it is rainy then close the windows >>',3,0),
	(11,'2014-02-05 14:52:33','Group 1 changed your room 2140 policy.','Some rules in group 1 have been changed. Since your room 2140 belongs to that group, you have to revalidate all your rules.',2,0),
	(12,'2014-02-05 14:52:33','Group 1 changed your room 2140 policy.','Some rules in group 1 have been changed. Since your room 2140 belongs to that group, you have to revalidate all your rules.',3,0),
	(13,'2014-02-05 14:52:33','Group 1 changed your room 2142 policy.','Some rules in group 1 have been changed. Since your room 2142 belongs to that group, you have to revalidate all your rules.',1,0),
	(14,'2014-02-05 14:52:33','Group 1 changed your room 2142 policy.','Some rules in group 1 have been changed. Since your room 2142 belongs to that group, you have to revalidate all your rules.',3,0);

/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rooms
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms`;

CREATE TABLE `rooms` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `description` longtext,
  PRIMARY KEY (`room_name`,`building_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;

INSERT INTO `rooms` (`room_name`, `building_name`, `description`)
VALUES
	('2140','CSE','Bharathan office'),
	('2142','CSE','Alessandro Office');

/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rooms_actions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms_actions`;

CREATE TABLE `rooms_actions` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `action_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`room_name`,`building_name`,`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rooms_actions` WRITE;
/*!40000 ALTER TABLE `rooms_actions` DISABLE KEYS */;

INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`)
VALUES
	('2140','CSE',1),
	('2140','CSE',2),
	('2140','CSE',3),
	('2140','CSE',4),
	('2140','CSE',5),
	('2140','CSE',6),
	('2140','CSE',7),
	('2140','CSE',8),
	('2140','CSE',9),
	('2140','CSE',10),
	('2142','CSE',1),
	('2142','CSE',2),
	('2142','CSE',3),
	('2142','CSE',4),
	('2142','CSE',5),
	('2142','CSE',6),
	('2142','CSE',7),
	('2142','CSE',8),
	('2142','CSE',9),
	('2142','CSE',10);

/*!40000 ALTER TABLE `rooms_actions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rooms_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms_groups`;

CREATE TABLE `rooms_groups` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `room_name` varchar(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`group_id`,`building_name`,`room_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rooms_groups` WRITE;
/*!40000 ALTER TABLE `rooms_groups` DISABLE KEYS */;

INSERT INTO `rooms_groups` (`group_id`, `building_name`, `room_name`)
VALUES
	(1,'CSE','2140'),
	(1,'CSE','2142'),
	(2,'CSE','2140'),
	(2,'CSE','2142');

/*!40000 ALTER TABLE `rooms_groups` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rooms_triggers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rooms_triggers`;

CREATE TABLE `rooms_triggers` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `trigger_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`room_name`,`building_name`,`trigger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rooms_triggers` WRITE;
/*!40000 ALTER TABLE `rooms_triggers` DISABLE KEYS */;

INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`)
VALUES
	('2140','CSE',1),
	('2140','CSE',2),
	('2140','CSE',5),
	('2140','CSE',8),
	('2140','CSE',9),
	('2140','CSE',10),
	('2140','CSE',11),
	('2140','CSE',12),
	('2140','CSE',13),
	('2140','CSE',14),
	('2140','CSE',15),
	('2142','CSE',1),
	('2142','CSE',2),
	('2142','CSE',5),
	('2142','CSE',8),
	('2142','CSE',9),
	('2142','CSE',10),
	('2142','CSE',11),
	('2142','CSE',12),
	('2142','CSE',13),
	('2142','CSE',14),
	('2142','CSE',15);

/*!40000 ALTER TABLE `rooms_triggers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rule_translation_dictionary
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rule_translation_dictionary`;

CREATE TABLE `rule_translation_dictionary` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `language` varchar(11) DEFAULT NULL,
  `original` varchar(255) DEFAULT NULL,
  `translation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rule_translation_dictionary` WRITE;
/*!40000 ALTER TABLE `rule_translation_dictionary` DISABLE KEYS */;

INSERT INTO `rule_translation_dictionary` (`id`, `language`, `original`, `translation`)
VALUES
	(1,'Z3','time is between @val and @val','(and (>= (time 1) @val) (<= (time 1) @val))'),
	(2,'Z3','someone is in the room','(inRoom 1)'),
	(3,'Z3','nodobdy is in the room','(not (inRoom 1))'),
	(4,'Z3','external temperature is between @val and @val','(and (>= (extTempInRoom 1) @val) (<= (extTempInRoom 1) @val))'),
	(5,'Z3','the date is between @val and @val','(and (>= (day 1) @val) (<= (day 1) @val))'),
	(6,'Z3','it is sunny','(sunny 1)'),
	(7,'Z3','it is rainy','(rainy 1)'),
	(8,'Z3','it is cloudy','(cloudy 1)'),
	(9,'Z3','room temperature is between @val and @val','(and (>= (tempInRoom 1) @val) (<= (tempInRoom 1) @val))'),
	(10,'Z3','turn on the light','(light 1)'),
	(11,'Z3','turn off the light','(not (light 1))'),
	(12,'Z3','turn on the heating','(heat 1)'),
	(13,'Z3','turn off the heating','(not (heat 1))'),
	(14,'Z3','turn on the cooling','(cool 1)'),
	(15,'Z3','turn off the cooling','(not (cool 1))'),
	(16,'Z3','open the windows','(openWindows 1)'),
	(17,'Z3','close the windows','(not (openWindows 1))'),
	(18,'Z3','open the curtains','(openCurtains 1)'),
	(19,'Z3','close the curtains','(not (openCurtains 1))'),
	(20,'Z3','no rule specified','(noRule 1)'),
	(21,'Z3','today is @val','(= (today 1) @val)');

/*!40000 ALTER TABLE `rule_translation_dictionary` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rules
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rules`;

CREATE TABLE `rules` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `priority` int(11) DEFAULT NULL,
  `category` varchar(24) DEFAULT NULL,
  `building_name` varchar(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `room_name` varchar(11) DEFAULT NULL,
  `author_uuid` int(11) DEFAULT NULL,
  `antecedent` varchar(255) DEFAULT NULL,
  `consequent` varchar(255) DEFAULT NULL,
  `enabled` int(1) DEFAULT NULL,
  `deleted` int(1) DEFAULT NULL,
  `creation_timestamp` timestamp NULL DEFAULT NULL,
  `last_edit_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rules` WRITE;
/*!40000 ALTER TABLE `rules` DISABLE KEYS */;

INSERT INTO `rules` (`id`, `priority`, `category`, `building_name`, `group_id`, `room_name`, `author_uuid`, `antecedent`, `consequent`, `enabled`, `deleted`, `creation_timestamp`, `last_edit_timestamp`)
VALUES
	(1,64,'HEATING','CSE',-1,'2142',1,'room temperature is between 60F and 70F','turn on the heating',0,0,'2014-02-05 14:44:55','2014-02-05 14:44:55'),
	(2,71,'WINDOWS','CSE',-1,'2142',1,'it is rainy','close the windows',0,0,'2014-02-05 14:45:13','2014-02-05 14:45:13'),
	(3,90,'HEATING','CSE',-1,'2142',1,'today is Sunday','turn on the heating',0,0,'2014-02-05 14:45:48','2014-02-05 14:45:48'),
	(4,97,'COOLING','CSE',-1,'2142',1,'today is Sunday','turn off the cooling',0,0,'2014-02-05 14:46:05','2014-02-05 14:46:05'),
	(5,92,'WINDOWS','CSE',-1,'2142',1,'today is Sunday','close the windows',0,0,'2014-02-05 14:46:19','2014-02-05 14:46:19'),
	(6,50,'LIGHT','CSE',-1,'2142',1,'today is Sunday','turn off the light',0,0,'2014-02-05 14:46:38','2014-02-05 14:46:38'),
	(7,50,'HEATING','CSE',-1,'2142',1,'external temperature is between 78F and 83F','turn on the heating',0,0,'2014-02-05 14:48:55','2014-02-05 14:48:55'),
	(8,0,'LIGHT','CSE',1,'None',3,'today is Sunday','turn off the light',1,0,'2014-02-05 14:52:33','2014-02-05 14:52:33');

/*!40000 ALTER TABLE `rules` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rules_priority
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rules_priority`;

CREATE TABLE `rules_priority` (
  `building_name` varchar(11) NOT NULL DEFAULT '0',
  `room_name` varchar(11) NOT NULL DEFAULT '0',
  `rule_id` int(11) NOT NULL DEFAULT '0',
  `rule_priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`building_name`,`room_name`,`rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rules_priority` WRITE;
/*!40000 ALTER TABLE `rules_priority` DISABLE KEYS */;

INSERT INTO `rules_priority` (`building_name`, `room_name`, `rule_id`, `rule_priority`)
VALUES
	('CSE','2142',1,64),
	('CSE','2142',2,100),
	('CSE','2142',3,80),
	('CSE','2142',4,80),
	('CSE','2142',5,80),
	('CSE','2142',6,80),
	('CSE','2142',7,50);

/*!40000 ALTER TABLE `rules_priority` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sessions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sessions`;

CREATE TABLE `sessions` (
  `session_key` varchar(64) NOT NULL DEFAULT '',
  `user_uuid` int(11) DEFAULT NULL,
  `expire_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;

INSERT INTO `sessions` (`session_key`, `user_uuid`, `expire_timestamp`)
VALUES
	('2E0BHS-b1bd283e62fbebccece6c2fa21c73d3b',3,'2014-02-06 14:52:44'),
	('L1YZXU-4bc1d77f33fee129f001affc660ad7ea',1,'2014-02-06 13:17:06'),
	('Y4K0WT-796ad46109eccabca80ec118ab10b92d',1,'2014-02-06 13:16:16'),
	('ZKIZAC-ff6651e2e2907ab97962ed374263f415',1,'2014-02-06 14:33:31');

/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table triggers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `triggers`;

CREATE TABLE `triggers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(16) DEFAULT NULL,
  `trigger_name` varchar(24) DEFAULT NULL,
  `rule_antecedent` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `triggers` WRITE;
/*!40000 ALTER TABLE `triggers` DISABLE KEYS */;

INSERT INTO `triggers` (`id`, `category`, `trigger_name`, `rule_antecedent`, `description`)
VALUES
	(1,'OCCUPANCY','OCCUPANCY_TRUE','someone is in the room','check if someone is in the room'),
	(2,'OCCUPANCY','OCCUPANCY_FALSE','nodobdy is in the room','check if nobody is in the room'),
	(5,'EXT_TEMPERATURE','EXT_TEMPERATURE_RANGE','external temperature is between @val and @val','check temperature'),
	(8,'TIME','TIME_RANGE','time is between @val and @val','check time'),
	(9,'DATE','DATE_RANGE','the date is between @val and @val','check day'),
	(10,'WEATHER','SUNNY','it is sunny','check the weather'),
	(11,'WEATHER','RAINY','it is rainy','check the weather'),
	(12,'ROOM_TEMPERATURE','ROOM_TEMPERATURE_RANGE','room temperature is between @val and @val','check temperature'),
	(13,'WEATHER','CLOUDY','it is cloudy','check the weather'),
	(14,'DEFAULT_STATUS','NO_RULE','no rule specified','default rule'),
	(15,'DAY','TODAY','today is @val','rules for the current day');

/*!40000 ALTER TABLE `triggers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `uuid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(11) NOT NULL DEFAULT '',
  `email` varchar(24) DEFAULT NULL,
  `password` varchar(24) DEFAULT NULL,
  `person_name` varchar(24) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`uuid`, `username`, `email`, `password`, `person_name`, `level`)
VALUES
	(1,'anacci','alenacci@gmail.com','alexnaccix','Alessandro Nacci',10),
	(2,'bbalaji','bbalaji@cs.ucsd.edu','bbalaji2014','Bharathan Balaji',10),
	(3,'admin','alenacci+admin@gmail.com','brules_admin_14','administrator',100);

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users_rooms
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users_rooms`;

CREATE TABLE `users_rooms` (
  `room_name` varchar(11) NOT NULL DEFAULT '',
  `building_name` varchar(11) NOT NULL DEFAULT '',
  `user_uuid` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`room_name`,`building_name`,`user_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `users_rooms` WRITE;
/*!40000 ALTER TABLE `users_rooms` DISABLE KEYS */;

INSERT INTO `users_rooms` (`room_name`, `building_name`, `user_uuid`)
VALUES
	('2140','CSE',2),
	('2140','CSE',3),
	('2142','CSE',1),
	('2142','CSE',3);

/*!40000 ALTER TABLE `users_rooms` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
