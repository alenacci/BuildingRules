# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.34-0ubuntu0.12.04.1)
# Database: building_rules
# Generation Time: 2014-01-31 03:02:11 +0000
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
  `action_name` varchar(11) DEFAULT NULL,
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
	(3,'HEATING','HEAT_ON','turn on the heating','turn on the heating'),
	(4,'HEATING','HEAT_OFF','turn off the heating','turn off the heating'),
	(5,'COOLING','COOL_ON','turn off the cooling','turn off the cooling'),
	(6,'COOLING','COOL_OFF','turn off the cooling','turn off the cooling');

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
	('EEE','Elect ','Booh');

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
	(5,'EEE','sad',1,'[\"LIGHT\"]');

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
	(9,'2014-01-30 18:35:59','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',1,1),
	(10,'2014-01-30 18:35:59','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',3,0),
	(11,'2014-01-30 18:48:38','Rule modified in building EEE room 300','The user alenacci edited (or tried to edit) the rule <<if it is rainy then turn on the light>>. The new rule is << if it is rainy then turn on the light >>',1,1),
	(12,'2014-01-30 18:48:38','Rule modified in building EEE room 300','The user alenacci edited (or tried to edit) the rule <<if it is rainy then turn on the light>>. The new rule is << if it is rainy then turn on the light >>',2,1),
	(13,'2014-01-30 18:48:38','Rule modified in building EEE room 300','The user alenacci edited (or tried to edit) the rule <<if it is rainy then turn on the light>>. The new rule is << if it is rainy then turn on the light >>',3,0),
	(14,'2014-01-30 18:49:34','Rule modified in building EEE room 200','The user guest edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',1,1),
	(15,'2014-01-30 18:49:34','Rule modified in building EEE room 200','The user guest edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',3,0),
	(16,'2014-01-30 18:52:35','Rule modified in building EEE room 200','The user guest edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',1,1),
	(17,'2014-01-30 18:52:35','Rule modified in building EEE room 200','The user guest edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',3,0),
	(18,'2014-01-30 18:54:33','Rule modified in building EEE group 5','The user guest edited (or tried to edit) the rule <<if temperature is between 10 and 1000 then turn off the heating>>. The new rule is << if temperature is between 10 and 1000 then turn off the heating >>',1,1),
	(19,'2014-01-30 18:54:33','Rule modified in building EEE group 5','The user guest edited (or tried to edit) the rule <<if temperature is between 10 and 1000 then turn off the heating>>. The new rule is << if temperature is between 10 and 1000 then turn off the heating >>',2,1),
	(20,'2014-01-30 18:54:33','Rule modified in building EEE group 5','The user guest edited (or tried to edit) the rule <<if temperature is between 10 and 1000 then turn off the heating>>. The new rule is << if temperature is between 10 and 1000 then turn off the heating >>',3,0),
	(21,'2014-01-30 18:57:23','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',1,1),
	(22,'2014-01-30 18:57:23','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',2,1),
	(23,'2014-01-30 18:57:23','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',3,0),
	(24,'2014-01-30 18:58:22','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',1,1),
	(25,'2014-01-30 18:58:22','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',2,1),
	(26,'2014-01-30 18:58:22','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',3,0),
	(27,'2014-01-30 19:01:15','Rule modified in building EEE room 500','The user guest edited (or tried to edit) the rule <<if temperature is between 10 and 22 then turn off the heating>>. The new rule is << if temperature is between 10 and 22 then turn off the heating >>',2,1),
	(28,'2014-01-30 19:01:15','Rule modified in building EEE room 500','The user guest edited (or tried to edit) the rule <<if temperature is between 10 and 22 then turn off the heating>>. The new rule is << if temperature is between 10 and 22 then turn off the heating >>',3,0),
	(29,'2014-01-30 19:01:50','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',1,1),
	(30,'2014-01-30 19:01:50','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',2,1),
	(31,'2014-01-30 19:01:50','Rule modified in building EEE room 200','The user alenacci edited (or tried to edit) the rule <<if it is sunny then turn on the light>>. The new rule is << if it is sunny then turn on the light >>',3,0);

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
	('200','EEE','Descr'),
	('300','EEE','Descr'),
	('400','EEE','Descr'),
	('500','EEE','Descr');

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
	('200','EEE',1),
	('200','EEE',2);

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
	(5,'EEE','200'),
	(5,'EEE','300'),
	(5,'EEE','400');

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
	(1,'Z3','it is between @val and @val','(and (> time @val) (< time @val))');

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
	(4,50,'UNKW','EEE',-1,'500',2,'temperature is between 10 and 22','turn off the heating',1,0,'2014-01-28 19:37:54','2014-01-28 19:37:54'),
	(11,50,'HEATING','EEE',-1,'200',1,'temperature is between 10 and 1000','turn off the heating',1,0,'2014-01-29 17:04:35','2014-01-29 17:04:35'),
	(15,50,'LIGHT','EEE',-1,'200',1,'it is sunny','turn on the light',1,0,'2014-01-29 19:39:34','2014-01-29 19:39:34'),
	(16,77,'LIGHT','EEE',-1,'300',1,'it is rainy','turn on the light',1,0,'2014-01-30 12:24:21','2014-01-30 12:24:21'),
	(17,100,'HEATING','EEE',5,'None',2,'temperature is between 10 and 1000','turn off the heating',1,0,'2014-01-30 18:53:23','2014-01-30 18:53:23');

/*!40000 ALTER TABLE `rules` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table rules_priority
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rules_priority`;

CREATE TABLE `rules_priority` (
  `building_name` varchar(11) NOT NULL DEFAULT '0',
  `room_name` int(11) NOT NULL DEFAULT '0',
  `rule_id` int(11) NOT NULL DEFAULT '0',
  `rule_priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`building_name`,`room_name`,`rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `rules_priority` WRITE;
/*!40000 ALTER TABLE `rules_priority` DISABLE KEYS */;

INSERT INTO `rules_priority` (`building_name`, `room_name`, `rule_id`, `rule_priority`)
VALUES
	('EEE',100,5,50),
	('EEE',100,17,100),
	('EEE',200,1,100),
	('EEE',200,7,6),
	('EEE',200,11,50),
	('EEE',200,12,50),
	('EEE',200,13,50),
	('EEE',200,14,10),
	('EEE',200,15,100),
	('EEE',300,2,91),
	('EEE',300,16,77),
	('EEE',500,3,68),
	('EEE',500,4,50);

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
	('JZMP8T-eb22c6a7067c4f46c0ed2b9efc786751',1,'2014-01-31 18:32:33'),
	('PCXQ31-2984b7ade3ee212c77e67c7b21ec1926',2,'2020-01-29 19:23:03'),
	('TWDWTS-e974377a11bf98c19699d6712ea27a0d',2,'2014-01-31 12:23:53'),
	('V5X3F1-7ee07458bfa24da9a1e227e3abd10406',1,'2014-01-31 18:32:53'),
	('YLKDKN-3a0d36aac017f896937e2df26e3f868f',1,'2014-01-31 17:59:34'),
	('Z724ZU-61f223cd185c2adafd5bf08ce060a4a6',1,'2014-01-30 19:27:53');

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
	(1,'PRESENCE','PRESENCE_TRUE','someone is','check if someone is in the room'),
	(2,'PRESENCE','PRESENCE_FALSE','anybody is','check if anyone is in the room'),
	(3,'TEMPERATURE','TEMPERATURE_HIGHER','temperature is higher than @val','check the temperature'),
	(4,'TEMPERATURE','TEMPERATURE_LOWER','temperature is lower than @val','check temperature'),
	(5,'TEMPERATURE','TEMPERATURE_RANGE','temperature is between @val and @val','check temperature'),
	(6,'TIME','TIME_AFTER','it is after @val | it is after @val','check time'),
	(7,'TIME','TIME_BEFORE','it is before @val | it is before @val','check time'),
	(8,'TIME','TIME_RANGE','it is between @val and @val','check time'),
	(9,'DATE','DATE_RANGE','it is between @val and @val','check day'),
	(10,'WEATHER','SUNNY','it is sunny','check the weather'),
	(11,'WEATHER','RAINY','it is rainy','check the weather');

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
	(1,'alenacci','alenacci@gmail.com','1234','Alessandro Nacci',6),
	(2,'guest','guest@brules.com','1234','Guest',6),
	(3,'admin','admin','admin','admin',100);

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
	('200','EEE',1),
	('200','EEE',3),
	('300','EEE',1),
	('300','EEE',2),
	('300','EEE',3),
	('400','EEE',1),
	('400','EEE',3),
	('500','EEE',2),
	('500','EEE',3);

/*!40000 ALTER TABLE `users_rooms` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
