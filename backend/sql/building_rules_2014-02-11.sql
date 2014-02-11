# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.34-0ubuntu0.12.04.1)
# Database: building_rules
# Generation Time: 2014-02-11 21:23:38 +0000
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


# Dump of table active_rules
# ------------------------------------------------------------

DROP TABLE IF EXISTS `active_rules`;

CREATE TABLE `active_rules` (
  `building_name` varchar(11) DEFAULT NULL,
  `room_name` varchar(11) DEFAULT NULL,
  `rule_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `active_rules` WRITE;
/*!40000 ALTER TABLE `active_rules` DISABLE KEYS */;

INSERT INTO `active_rules` (`building_name`, `room_name`, `rule_id`)
VALUES
	('CSE','2107',2),
	('CSE','2107',1);

/*!40000 ALTER TABLE `active_rules` ENABLE KEYS */;
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
	(1,'CSE','Administrator Group',0,'[]'),
	(2,'CSE','Room Group A',0,'[]'),
	(3,'CSE','Room Group B',0,'[]'),
	(4,'CSE','Thermal Zone 1',1,'[\"HEATING\"]'),
	(5,'CSE','Thermal Zone 2',1,'[\"HEATING\"]'),
	(6,'CSE','Thermal Zone 3',1,'[\"HEATING\"]'),
	(7,'CSE','Thermal Zone 4',1,'[\"HEATING\"]'),
	(8,'CSE','Thermal Zone 5',1,'[\"HEATING\"]'),
	(9,'CSE','Thermal Zone 6',1,'[\"HEATING\"]'),
	(10,'CSE','Thermal Zone 7',1,'[\"HEATING\"]');

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
	(1,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',1,0),
	(2,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',2,0),
	(3,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',3,0),
	(4,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',4,0),
	(5,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',5,0),
	(6,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',6,0),
	(7,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',7,1),
	(8,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',8,0),
	(9,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',9,0),
	(10,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',10,0),
	(11,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',11,0),
	(12,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',12,0),
	(13,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',13,0),
	(14,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',14,0),
	(15,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',15,0),
	(16,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',16,0),
	(17,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',17,0),
	(18,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',18,0),
	(19,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',19,0),
	(20,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',20,0),
	(21,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',21,0),
	(22,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',22,0),
	(23,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',23,0),
	(24,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',24,0),
	(25,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',25,0),
	(26,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',26,0),
	(27,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',27,0),
	(28,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',28,0),
	(29,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',29,0),
	(30,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',30,0),
	(31,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',31,0),
	(32,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',32,0),
	(33,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',33,0),
	(34,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',34,0),
	(35,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',35,0),
	(36,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',36,0),
	(37,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',37,0),
	(38,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',38,0),
	(39,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',39,0),
	(40,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',40,0),
	(41,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',41,0),
	(42,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',42,0),
	(43,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',43,0),
	(44,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',44,0),
	(45,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',45,0),
	(46,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',46,0),
	(47,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',47,0),
	(48,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',48,0),
	(49,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',49,0),
	(50,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',50,0),
	(51,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',51,0),
	(52,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',52,0),
	(53,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',53,0),
	(54,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',54,0),
	(55,'2014-02-11 12:55:32','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if someone is in the room then turn off the heating>>. The new rule is <<if today is Tuesday then turn on the light>>',55,0),
	(56,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',1,0),
	(57,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',2,0),
	(58,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',3,0),
	(59,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',4,0),
	(60,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',5,0),
	(61,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',6,0),
	(62,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',7,1),
	(63,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',8,0),
	(64,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',9,0),
	(65,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',10,0),
	(66,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',11,0),
	(67,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',12,0),
	(68,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',13,0),
	(69,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',14,0),
	(70,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',15,0),
	(71,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',16,0),
	(72,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',17,0),
	(73,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',18,0),
	(74,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',19,0),
	(75,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',20,0),
	(76,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',21,0),
	(77,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',22,0),
	(78,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',23,0),
	(79,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',24,0),
	(80,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',25,0),
	(81,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',26,0),
	(82,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',27,0),
	(83,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',28,0),
	(84,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',29,0),
	(85,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',30,0),
	(86,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',31,0),
	(87,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',32,0),
	(88,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',33,0),
	(89,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',34,0),
	(90,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',35,0),
	(91,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',36,0),
	(92,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',37,0),
	(93,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',38,0),
	(94,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',39,0),
	(95,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',40,0),
	(96,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',41,0),
	(97,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',42,0),
	(98,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',43,0),
	(99,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',44,0),
	(100,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',45,0),
	(101,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',46,0),
	(102,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',47,0),
	(103,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',48,0),
	(104,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',49,0),
	(105,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',50,0),
	(106,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',51,0),
	(107,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',52,0),
	(108,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',53,0),
	(109,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',54,0),
	(110,'2014-02-11 13:20:53','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Wednesday then turn on the cooling>>. The new rule is <<if today is Monday then turn off the cooling>>',55,0),
	(111,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',1,0),
	(112,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',2,0),
	(113,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',3,0),
	(114,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',4,0),
	(115,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',5,0),
	(116,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',6,0),
	(117,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',7,1),
	(118,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',8,0),
	(119,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',9,0),
	(120,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',10,0),
	(121,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',11,0),
	(122,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',12,0),
	(123,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',13,0),
	(124,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',14,0),
	(125,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',15,0),
	(126,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',16,0),
	(127,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',17,0),
	(128,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',18,0),
	(129,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',19,0),
	(130,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',20,0),
	(131,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',21,0),
	(132,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',22,0),
	(133,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',23,0),
	(134,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',24,0),
	(135,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',25,0),
	(136,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',26,0),
	(137,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',27,0),
	(138,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',28,0),
	(139,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',29,0),
	(140,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',30,0),
	(141,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',31,0),
	(142,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',32,0),
	(143,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',33,0),
	(144,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',34,0),
	(145,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',35,0),
	(146,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',36,0),
	(147,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',37,0),
	(148,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',38,0),
	(149,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',39,0),
	(150,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',40,0),
	(151,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',41,0),
	(152,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',42,0),
	(153,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',43,0),
	(154,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',44,0),
	(155,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',45,0),
	(156,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',46,0),
	(157,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',47,0),
	(158,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',48,0),
	(159,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',49,0),
	(160,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',50,0),
	(161,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',51,0),
	(162,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',52,0),
	(163,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',53,0),
	(164,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',54,0),
	(165,'2014-02-11 13:21:12','Rule modified in building CSE room 2107','The user e edited (or tried to edit) the rule <<if today is Monday then turn off the cooling>>. The new rule is <<if today is Tuesday then turn off the cooling>>',55,0);

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
	('2107','CSE','Kitchen'),
	('2108','CSE','Office Room'),
	('2109','CSE','Lobby'),
	('2111','CSE','Office Room'),
	('2112','CSE','Office Room'),
	('2116','CSE','Office Room'),
	('2118','CSE','Office Room'),
	('2122','CSE','Office Room'),
	('2126','CSE','Office Room'),
	('2128','CSE','Office Room'),
	('2132','CSE','Office Room'),
	('2134','CSE','Office Room'),
	('2136','CSE','Office Room'),
	('2138','CSE','Office Room'),
	('2140','CSE','Meeting Room'),
	('2144','CSE','Storage'),
	('2154','CSE','Meeting Room'),
	('2203','CSE','Office Room'),
	('2215','CSE','Office Room'),
	('2217','CSE','Office Room'),
	('2230','CSE','Study Room'),
	('2231','CSE','Office Room'),
	('3113','CSE','Laboratory'),
	('3208','CSE','Conference Room');

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
	('2107','CSE',1),
	('2107','CSE',2),
	('2107','CSE',3),
	('2107','CSE',4),
	('2107','CSE',5),
	('2107','CSE',6),
	('2107','CSE',7),
	('2107','CSE',8),
	('2107','CSE',9),
	('2107','CSE',10),
	('2108','CSE',1),
	('2108','CSE',2),
	('2108','CSE',3),
	('2108','CSE',4),
	('2108','CSE',5),
	('2108','CSE',6),
	('2108','CSE',7),
	('2108','CSE',8),
	('2108','CSE',9),
	('2108','CSE',10),
	('2109','CSE',1),
	('2109','CSE',2),
	('2109','CSE',3),
	('2109','CSE',4),
	('2109','CSE',5),
	('2109','CSE',6),
	('2109','CSE',7),
	('2109','CSE',8),
	('2109','CSE',9),
	('2109','CSE',10),
	('2111','CSE',1),
	('2111','CSE',2),
	('2111','CSE',3),
	('2111','CSE',4),
	('2111','CSE',5),
	('2111','CSE',6),
	('2111','CSE',7),
	('2111','CSE',8),
	('2111','CSE',9),
	('2111','CSE',10),
	('2112','CSE',1),
	('2112','CSE',2),
	('2112','CSE',3),
	('2112','CSE',4),
	('2112','CSE',5),
	('2112','CSE',6),
	('2112','CSE',7),
	('2112','CSE',8),
	('2112','CSE',9),
	('2112','CSE',10),
	('2116','CSE',1),
	('2116','CSE',2),
	('2116','CSE',3),
	('2116','CSE',4),
	('2116','CSE',5),
	('2116','CSE',6),
	('2116','CSE',7),
	('2116','CSE',8),
	('2116','CSE',9),
	('2116','CSE',10),
	('2118','CSE',1),
	('2118','CSE',2),
	('2118','CSE',3),
	('2118','CSE',4),
	('2118','CSE',5),
	('2118','CSE',6),
	('2118','CSE',7),
	('2118','CSE',8),
	('2118','CSE',9),
	('2118','CSE',10),
	('2122','CSE',1),
	('2122','CSE',2),
	('2122','CSE',3),
	('2122','CSE',4),
	('2122','CSE',5),
	('2122','CSE',6),
	('2122','CSE',7),
	('2122','CSE',8),
	('2122','CSE',9),
	('2122','CSE',10),
	('2126','CSE',1),
	('2126','CSE',2),
	('2126','CSE',3),
	('2126','CSE',4),
	('2126','CSE',5),
	('2126','CSE',6),
	('2126','CSE',7),
	('2126','CSE',8),
	('2126','CSE',9),
	('2126','CSE',10),
	('2128','CSE',1),
	('2128','CSE',2),
	('2128','CSE',3),
	('2128','CSE',4),
	('2128','CSE',5),
	('2128','CSE',6),
	('2128','CSE',7),
	('2128','CSE',8),
	('2128','CSE',9),
	('2128','CSE',10),
	('2132','CSE',1),
	('2132','CSE',2),
	('2132','CSE',3),
	('2132','CSE',4),
	('2132','CSE',5),
	('2132','CSE',6),
	('2132','CSE',7),
	('2132','CSE',8),
	('2132','CSE',9),
	('2132','CSE',10),
	('2134','CSE',1),
	('2134','CSE',2),
	('2134','CSE',3),
	('2134','CSE',4),
	('2134','CSE',5),
	('2134','CSE',6),
	('2134','CSE',7),
	('2134','CSE',8),
	('2134','CSE',9),
	('2134','CSE',10),
	('2136','CSE',1),
	('2136','CSE',2),
	('2136','CSE',3),
	('2136','CSE',4),
	('2136','CSE',5),
	('2136','CSE',6),
	('2136','CSE',7),
	('2136','CSE',8),
	('2136','CSE',9),
	('2136','CSE',10),
	('2138','CSE',1),
	('2138','CSE',2),
	('2138','CSE',3),
	('2138','CSE',4),
	('2138','CSE',5),
	('2138','CSE',6),
	('2138','CSE',7),
	('2138','CSE',8),
	('2138','CSE',9),
	('2138','CSE',10),
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
	('2144','CSE',1),
	('2144','CSE',2),
	('2144','CSE',3),
	('2144','CSE',4),
	('2144','CSE',5),
	('2144','CSE',6),
	('2144','CSE',7),
	('2144','CSE',8),
	('2144','CSE',9),
	('2144','CSE',10),
	('2154','CSE',1),
	('2154','CSE',2),
	('2154','CSE',3),
	('2154','CSE',4),
	('2154','CSE',5),
	('2154','CSE',6),
	('2154','CSE',7),
	('2154','CSE',8),
	('2154','CSE',9),
	('2154','CSE',10),
	('2203','CSE',1),
	('2203','CSE',2),
	('2203','CSE',3),
	('2203','CSE',4),
	('2203','CSE',5),
	('2203','CSE',6),
	('2203','CSE',7),
	('2203','CSE',8),
	('2203','CSE',9),
	('2203','CSE',10),
	('2215','CSE',1),
	('2215','CSE',2),
	('2215','CSE',3),
	('2215','CSE',4),
	('2215','CSE',5),
	('2215','CSE',6),
	('2215','CSE',7),
	('2215','CSE',8),
	('2215','CSE',9),
	('2215','CSE',10),
	('2217','CSE',1),
	('2217','CSE',2),
	('2217','CSE',3),
	('2217','CSE',4),
	('2217','CSE',5),
	('2217','CSE',6),
	('2217','CSE',7),
	('2217','CSE',8),
	('2217','CSE',9),
	('2217','CSE',10),
	('2230','CSE',1),
	('2230','CSE',2),
	('2230','CSE',3),
	('2230','CSE',4),
	('2230','CSE',5),
	('2230','CSE',6),
	('2230','CSE',7),
	('2230','CSE',8),
	('2230','CSE',9),
	('2230','CSE',10),
	('2231','CSE',1),
	('2231','CSE',2),
	('2231','CSE',3),
	('2231','CSE',4),
	('2231','CSE',5),
	('2231','CSE',6),
	('2231','CSE',7),
	('2231','CSE',8),
	('2231','CSE',9),
	('2231','CSE',10),
	('3113','CSE',1),
	('3113','CSE',2),
	('3113','CSE',3),
	('3113','CSE',4),
	('3113','CSE',5),
	('3113','CSE',6),
	('3113','CSE',7),
	('3113','CSE',8),
	('3113','CSE',9),
	('3113','CSE',10),
	('3208','CSE',1),
	('3208','CSE',2),
	('3208','CSE',3),
	('3208','CSE',4),
	('3208','CSE',5),
	('3208','CSE',6),
	('3208','CSE',7),
	('3208','CSE',8),
	('3208','CSE',9),
	('3208','CSE',10);

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
	(1,'CSE','2107'),
	(1,'CSE','2108'),
	(1,'CSE','2109'),
	(1,'CSE','2111'),
	(1,'CSE','2112'),
	(1,'CSE','2116'),
	(1,'CSE','2118'),
	(1,'CSE','2122'),
	(1,'CSE','2126'),
	(1,'CSE','2128'),
	(1,'CSE','2132'),
	(1,'CSE','2134'),
	(1,'CSE','2136'),
	(1,'CSE','2138'),
	(1,'CSE','2140'),
	(1,'CSE','2144'),
	(1,'CSE','2154'),
	(1,'CSE','2203'),
	(1,'CSE','2215'),
	(1,'CSE','2217'),
	(1,'CSE','2230'),
	(1,'CSE','2231'),
	(1,'CSE','3113'),
	(1,'CSE','3208'),
	(2,'CSE','2108'),
	(2,'CSE','2111'),
	(2,'CSE','2112'),
	(2,'CSE','2116'),
	(2,'CSE','2118'),
	(2,'CSE','2122'),
	(2,'CSE','2126'),
	(2,'CSE','2128'),
	(3,'CSE','2132'),
	(3,'CSE','2134'),
	(3,'CSE','2136'),
	(3,'CSE','2138'),
	(3,'CSE','2203'),
	(3,'CSE','2215'),
	(3,'CSE','2217'),
	(3,'CSE','2231'),
	(4,'CSE','2108'),
	(4,'CSE','2112'),
	(5,'CSE','2111'),
	(5,'CSE','2116'),
	(6,'CSE','2118'),
	(6,'CSE','2122'),
	(7,'CSE','2132'),
	(7,'CSE','2134'),
	(8,'CSE','2136'),
	(8,'CSE','2138'),
	(8,'CSE','2231'),
	(9,'CSE','2203'),
	(9,'CSE','2215'),
	(9,'CSE','2217'),
	(10,'CSE','2107'),
	(10,'CSE','2144');

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
	('2107','CSE',1),
	('2107','CSE',2),
	('2107','CSE',5),
	('2107','CSE',8),
	('2107','CSE',9),
	('2107','CSE',10),
	('2107','CSE',11),
	('2107','CSE',12),
	('2107','CSE',13),
	('2107','CSE',14),
	('2107','CSE',15),
	('2108','CSE',1),
	('2108','CSE',2),
	('2108','CSE',5),
	('2108','CSE',8),
	('2108','CSE',9),
	('2108','CSE',10),
	('2108','CSE',11),
	('2108','CSE',12),
	('2108','CSE',13),
	('2108','CSE',14),
	('2108','CSE',15),
	('2109','CSE',1),
	('2109','CSE',2),
	('2109','CSE',5),
	('2109','CSE',8),
	('2109','CSE',9),
	('2109','CSE',10),
	('2109','CSE',11),
	('2109','CSE',12),
	('2109','CSE',13),
	('2109','CSE',14),
	('2109','CSE',15),
	('2111','CSE',1),
	('2111','CSE',2),
	('2111','CSE',5),
	('2111','CSE',8),
	('2111','CSE',9),
	('2111','CSE',10),
	('2111','CSE',11),
	('2111','CSE',12),
	('2111','CSE',13),
	('2111','CSE',14),
	('2111','CSE',15),
	('2112','CSE',1),
	('2112','CSE',2),
	('2112','CSE',5),
	('2112','CSE',8),
	('2112','CSE',9),
	('2112','CSE',10),
	('2112','CSE',11),
	('2112','CSE',12),
	('2112','CSE',13),
	('2112','CSE',14),
	('2112','CSE',15),
	('2116','CSE',1),
	('2116','CSE',2),
	('2116','CSE',5),
	('2116','CSE',8),
	('2116','CSE',9),
	('2116','CSE',10),
	('2116','CSE',11),
	('2116','CSE',12),
	('2116','CSE',13),
	('2116','CSE',14),
	('2116','CSE',15),
	('2118','CSE',1),
	('2118','CSE',2),
	('2118','CSE',5),
	('2118','CSE',8),
	('2118','CSE',9),
	('2118','CSE',10),
	('2118','CSE',11),
	('2118','CSE',12),
	('2118','CSE',13),
	('2118','CSE',14),
	('2118','CSE',15),
	('2122','CSE',1),
	('2122','CSE',2),
	('2122','CSE',5),
	('2122','CSE',8),
	('2122','CSE',9),
	('2122','CSE',10),
	('2122','CSE',11),
	('2122','CSE',12),
	('2122','CSE',13),
	('2122','CSE',14),
	('2122','CSE',15),
	('2126','CSE',1),
	('2126','CSE',2),
	('2126','CSE',5),
	('2126','CSE',8),
	('2126','CSE',9),
	('2126','CSE',10),
	('2126','CSE',11),
	('2126','CSE',12),
	('2126','CSE',13),
	('2126','CSE',14),
	('2126','CSE',15),
	('2128','CSE',1),
	('2128','CSE',2),
	('2128','CSE',5),
	('2128','CSE',8),
	('2128','CSE',9),
	('2128','CSE',10),
	('2128','CSE',11),
	('2128','CSE',12),
	('2128','CSE',13),
	('2128','CSE',14),
	('2128','CSE',15),
	('2132','CSE',1),
	('2132','CSE',2),
	('2132','CSE',5),
	('2132','CSE',8),
	('2132','CSE',9),
	('2132','CSE',10),
	('2132','CSE',11),
	('2132','CSE',12),
	('2132','CSE',13),
	('2132','CSE',14),
	('2132','CSE',15),
	('2134','CSE',1),
	('2134','CSE',2),
	('2134','CSE',5),
	('2134','CSE',8),
	('2134','CSE',9),
	('2134','CSE',10),
	('2134','CSE',11),
	('2134','CSE',12),
	('2134','CSE',13),
	('2134','CSE',14),
	('2134','CSE',15),
	('2136','CSE',1),
	('2136','CSE',2),
	('2136','CSE',5),
	('2136','CSE',8),
	('2136','CSE',9),
	('2136','CSE',10),
	('2136','CSE',11),
	('2136','CSE',12),
	('2136','CSE',13),
	('2136','CSE',14),
	('2136','CSE',15),
	('2138','CSE',1),
	('2138','CSE',2),
	('2138','CSE',5),
	('2138','CSE',8),
	('2138','CSE',9),
	('2138','CSE',10),
	('2138','CSE',11),
	('2138','CSE',12),
	('2138','CSE',13),
	('2138','CSE',14),
	('2138','CSE',15),
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
	('2144','CSE',1),
	('2144','CSE',2),
	('2144','CSE',5),
	('2144','CSE',8),
	('2144','CSE',9),
	('2144','CSE',10),
	('2144','CSE',11),
	('2144','CSE',12),
	('2144','CSE',13),
	('2144','CSE',14),
	('2144','CSE',15),
	('2154','CSE',1),
	('2154','CSE',2),
	('2154','CSE',5),
	('2154','CSE',8),
	('2154','CSE',9),
	('2154','CSE',10),
	('2154','CSE',11),
	('2154','CSE',12),
	('2154','CSE',13),
	('2154','CSE',14),
	('2154','CSE',15),
	('2203','CSE',1),
	('2203','CSE',2),
	('2203','CSE',5),
	('2203','CSE',8),
	('2203','CSE',9),
	('2203','CSE',10),
	('2203','CSE',11),
	('2203','CSE',12),
	('2203','CSE',13),
	('2203','CSE',14),
	('2203','CSE',15),
	('2215','CSE',1),
	('2215','CSE',2),
	('2215','CSE',5),
	('2215','CSE',8),
	('2215','CSE',9),
	('2215','CSE',10),
	('2215','CSE',11),
	('2215','CSE',12),
	('2215','CSE',13),
	('2215','CSE',14),
	('2215','CSE',15),
	('2217','CSE',1),
	('2217','CSE',2),
	('2217','CSE',5),
	('2217','CSE',8),
	('2217','CSE',9),
	('2217','CSE',10),
	('2217','CSE',11),
	('2217','CSE',12),
	('2217','CSE',13),
	('2217','CSE',14),
	('2217','CSE',15),
	('2230','CSE',1),
	('2230','CSE',2),
	('2230','CSE',5),
	('2230','CSE',8),
	('2230','CSE',9),
	('2230','CSE',10),
	('2230','CSE',11),
	('2230','CSE',12),
	('2230','CSE',13),
	('2230','CSE',14),
	('2230','CSE',15),
	('2231','CSE',1),
	('2231','CSE',2),
	('2231','CSE',5),
	('2231','CSE',8),
	('2231','CSE',9),
	('2231','CSE',10),
	('2231','CSE',11),
	('2231','CSE',12),
	('2231','CSE',13),
	('2231','CSE',14),
	('2231','CSE',15),
	('3113','CSE',1),
	('3113','CSE',2),
	('3113','CSE',5),
	('3113','CSE',8),
	('3113','CSE',9),
	('3113','CSE',10),
	('3113','CSE',11),
	('3113','CSE',12),
	('3113','CSE',13),
	('3113','CSE',14),
	('3113','CSE',15),
	('3208','CSE',1),
	('3208','CSE',2),
	('3208','CSE',5),
	('3208','CSE',8),
	('3208','CSE',9),
	('3208','CSE',10),
	('3208','CSE',11),
	('3208','CSE',12),
	('3208','CSE',13),
	('3208','CSE',14),
	('3208','CSE',15);

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
	(1,50,'HEATING','CSE',-1,'2107',7,'today is Tuesday','turn on the light',1,0,'2014-02-11 12:30:48','2014-02-11 12:30:48'),
	(2,50,'COOLING','CSE',-1,'2107',7,'today is Tuesday','turn off the cooling',1,0,'2014-02-11 13:13:36','2014-02-11 13:13:36');

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
	('CSE','2107',1,50),
	('CSE','2107',2,66);

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
	('2DJFM0-28299a83c27091b403f8506113c25978',3,'2014-02-12 12:11:04');

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
  `email` varchar(64) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `person_name` varchar(24) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`uuid`, `username`, `email`, `password`, `person_name`, `level`)
VALUES
	(1,'admin','energybox.buildingrules@gmail.com','brulesAdmin2014','Administrator',100),
	(2,'c','c','c','c',10),
	(3,'a','a','a','a',10),
	(4,'b','b','b','b',10),
	(5,'q','q','q','q',10),
	(6,'w','w','w','w',10),
	(7,'e','e','e','ee',10),
	(8,'user_6','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User6',10),
	(9,'user_7','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User7',10),
	(10,'user_8','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User8',10),
	(11,'user_9','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User9',10),
	(12,'user_10','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User10',10),
	(13,'user_11','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User11',10),
	(14,'user_12','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User12',10),
	(15,'user_13','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User13',10),
	(16,'user_14','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User14',10),
	(17,'user_15','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User15',10),
	(18,'user_16','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User16',10),
	(19,'user_17','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User17',10),
	(20,'user_18','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User18',10),
	(21,'user_19','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User19',10),
	(22,'user_20','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User20',10),
	(23,'user_21','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User21',10),
	(24,'user_22','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User22',10),
	(25,'user_23','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User23',10),
	(26,'user_24','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User24',10),
	(27,'user_25','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User25',10),
	(28,'user_26','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User26',10),
	(29,'user_27','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User27',10),
	(30,'user_28','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User28',10),
	(31,'user_29','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User29',10),
	(32,'user_30','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User30',10),
	(33,'user_31','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User31',10),
	(34,'user_32','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User32',10),
	(35,'user_33','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User33',10),
	(36,'user_34','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User34',10),
	(37,'user_35','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User35',10),
	(38,'user_36','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User36',10),
	(39,'user_37','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User37',10),
	(40,'user_38','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User38',10),
	(41,'user_39','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User39',10),
	(42,'user_40','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User40',10),
	(43,'user_41','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User41',10),
	(44,'user_42','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User42',10),
	(45,'user_43','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User43',10),
	(46,'user_44','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User44',10),
	(47,'user_45','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User45',10),
	(48,'user_46','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User46',10),
	(49,'user_47','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User47',10),
	(50,'user_48','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User48',10),
	(51,'user_49','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User49',10),
	(52,'user_50','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User50',10),
	(53,'user_51','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User51',10),
	(54,'user_52','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User52',10),
	(55,'user_53','--','verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword','User53',10);

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
	('2107','CSE',1),
	('2107','CSE',2),
	('2107','CSE',3),
	('2107','CSE',4),
	('2107','CSE',5),
	('2107','CSE',6),
	('2107','CSE',7),
	('2107','CSE',8),
	('2107','CSE',9),
	('2107','CSE',10),
	('2107','CSE',11),
	('2107','CSE',12),
	('2107','CSE',13),
	('2107','CSE',14),
	('2107','CSE',15),
	('2107','CSE',16),
	('2107','CSE',17),
	('2107','CSE',18),
	('2107','CSE',19),
	('2107','CSE',20),
	('2107','CSE',21),
	('2107','CSE',22),
	('2107','CSE',23),
	('2107','CSE',24),
	('2107','CSE',25),
	('2107','CSE',26),
	('2107','CSE',27),
	('2107','CSE',28),
	('2107','CSE',29),
	('2107','CSE',30),
	('2107','CSE',31),
	('2107','CSE',32),
	('2107','CSE',33),
	('2107','CSE',34),
	('2107','CSE',35),
	('2107','CSE',36),
	('2107','CSE',37),
	('2107','CSE',38),
	('2107','CSE',39),
	('2107','CSE',40),
	('2107','CSE',41),
	('2107','CSE',42),
	('2107','CSE',43),
	('2107','CSE',44),
	('2107','CSE',45),
	('2107','CSE',46),
	('2107','CSE',47),
	('2107','CSE',48),
	('2107','CSE',49),
	('2107','CSE',50),
	('2107','CSE',51),
	('2107','CSE',52),
	('2107','CSE',53),
	('2107','CSE',54),
	('2107','CSE',55),
	('2108','CSE',1),
	('2108','CSE',52),
	('2109','CSE',1),
	('2109','CSE',2),
	('2109','CSE',3),
	('2109','CSE',4),
	('2109','CSE',5),
	('2109','CSE',6),
	('2109','CSE',7),
	('2109','CSE',8),
	('2109','CSE',9),
	('2109','CSE',10),
	('2109','CSE',11),
	('2109','CSE',12),
	('2109','CSE',13),
	('2109','CSE',14),
	('2109','CSE',15),
	('2109','CSE',16),
	('2109','CSE',17),
	('2109','CSE',18),
	('2109','CSE',19),
	('2109','CSE',20),
	('2109','CSE',21),
	('2109','CSE',22),
	('2109','CSE',23),
	('2109','CSE',24),
	('2109','CSE',25),
	('2109','CSE',26),
	('2109','CSE',27),
	('2109','CSE',28),
	('2109','CSE',29),
	('2109','CSE',30),
	('2109','CSE',31),
	('2109','CSE',32),
	('2109','CSE',33),
	('2109','CSE',34),
	('2109','CSE',35),
	('2109','CSE',36),
	('2109','CSE',37),
	('2109','CSE',38),
	('2109','CSE',39),
	('2109','CSE',40),
	('2109','CSE',41),
	('2109','CSE',42),
	('2109','CSE',43),
	('2109','CSE',44),
	('2109','CSE',45),
	('2109','CSE',46),
	('2109','CSE',47),
	('2109','CSE',48),
	('2109','CSE',49),
	('2109','CSE',50),
	('2109','CSE',51),
	('2109','CSE',52),
	('2109','CSE',53),
	('2109','CSE',54),
	('2109','CSE',55),
	('2111','CSE',1),
	('2111','CSE',53),
	('2111','CSE',54),
	('2111','CSE',55),
	('2112','CSE',1),
	('2112','CSE',2),
	('2112','CSE',3),
	('2112','CSE',4),
	('2112','CSE',5),
	('2112','CSE',6),
	('2116','CSE',1),
	('2116','CSE',7),
	('2116','CSE',8),
	('2116','CSE',9),
	('2118','CSE',1),
	('2118','CSE',10),
	('2122','CSE',1),
	('2122','CSE',17),
	('2122','CSE',18),
	('2122','CSE',19),
	('2122','CSE',20),
	('2122','CSE',21),
	('2122','CSE',22),
	('2122','CSE',23),
	('2126','CSE',1),
	('2126','CSE',24),
	('2128','CSE',1),
	('2128','CSE',25),
	('2128','CSE',26),
	('2128','CSE',27),
	('2128','CSE',28),
	('2128','CSE',29),
	('2128','CSE',30),
	('2128','CSE',31),
	('2128','CSE',32),
	('2128','CSE',33),
	('2132','CSE',1),
	('2132','CSE',34),
	('2132','CSE',35),
	('2132','CSE',36),
	('2134','CSE',1),
	('2134','CSE',37),
	('2134','CSE',38),
	('2134','CSE',39),
	('2136','CSE',1),
	('2136','CSE',41),
	('2136','CSE',42),
	('2136','CSE',43),
	('2138','CSE',1),
	('2138','CSE',44),
	('2138','CSE',45),
	('2138','CSE',46),
	('2138','CSE',47),
	('2138','CSE',48),
	('2138','CSE',49),
	('2138','CSE',50),
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
	('2140','CSE',17),
	('2140','CSE',18),
	('2140','CSE',19),
	('2140','CSE',20),
	('2140','CSE',21),
	('2140','CSE',22),
	('2140','CSE',23),
	('2140','CSE',24),
	('2140','CSE',25),
	('2140','CSE',26),
	('2140','CSE',27),
	('2140','CSE',28),
	('2140','CSE',29),
	('2140','CSE',30),
	('2140','CSE',31),
	('2140','CSE',32),
	('2140','CSE',33),
	('2140','CSE',52),
	('2140','CSE',53),
	('2140','CSE',54),
	('2140','CSE',55),
	('2144','CSE',1),
	('2144','CSE',2),
	('2144','CSE',3),
	('2144','CSE',4),
	('2144','CSE',5),
	('2144','CSE',6),
	('2144','CSE',7),
	('2144','CSE',8),
	('2144','CSE',9),
	('2144','CSE',10),
	('2144','CSE',11),
	('2144','CSE',12),
	('2144','CSE',13),
	('2144','CSE',14),
	('2144','CSE',15),
	('2144','CSE',16),
	('2144','CSE',17),
	('2144','CSE',18),
	('2144','CSE',19),
	('2144','CSE',20),
	('2144','CSE',21),
	('2144','CSE',22),
	('2144','CSE',23),
	('2144','CSE',24),
	('2144','CSE',25),
	('2144','CSE',26),
	('2144','CSE',27),
	('2144','CSE',28),
	('2144','CSE',29),
	('2144','CSE',30),
	('2144','CSE',31),
	('2144','CSE',32),
	('2144','CSE',33),
	('2144','CSE',34),
	('2144','CSE',35),
	('2144','CSE',36),
	('2144','CSE',37),
	('2144','CSE',38),
	('2144','CSE',39),
	('2144','CSE',40),
	('2144','CSE',41),
	('2144','CSE',42),
	('2144','CSE',43),
	('2144','CSE',44),
	('2144','CSE',45),
	('2144','CSE',46),
	('2144','CSE',47),
	('2144','CSE',48),
	('2144','CSE',49),
	('2144','CSE',50),
	('2144','CSE',51),
	('2144','CSE',52),
	('2144','CSE',53),
	('2144','CSE',54),
	('2144','CSE',55),
	('2154','CSE',1),
	('2154','CSE',11),
	('2154','CSE',12),
	('2154','CSE',13),
	('2154','CSE',14),
	('2154','CSE',15),
	('2154','CSE',16),
	('2154','CSE',34),
	('2154','CSE',35),
	('2154','CSE',36),
	('2154','CSE',37),
	('2154','CSE',38),
	('2154','CSE',39),
	('2154','CSE',40),
	('2154','CSE',41),
	('2154','CSE',42),
	('2154','CSE',43),
	('2154','CSE',44),
	('2154','CSE',45),
	('2154','CSE',46),
	('2154','CSE',47),
	('2154','CSE',48),
	('2154','CSE',49),
	('2154','CSE',50),
	('2154','CSE',51),
	('2203','CSE',1),
	('2203','CSE',51),
	('2215','CSE',1),
	('2215','CSE',11),
	('2215','CSE',12),
	('2215','CSE',13),
	('2215','CSE',14),
	('2215','CSE',15),
	('2217','CSE',1),
	('2217','CSE',16),
	('2230','CSE',1),
	('2230','CSE',2),
	('2230','CSE',3),
	('2230','CSE',4),
	('2230','CSE',5),
	('2230','CSE',6),
	('2230','CSE',7),
	('2230','CSE',8),
	('2230','CSE',9),
	('2230','CSE',10),
	('2230','CSE',11),
	('2230','CSE',12),
	('2230','CSE',13),
	('2230','CSE',14),
	('2230','CSE',15),
	('2230','CSE',16),
	('2230','CSE',17),
	('2230','CSE',18),
	('2230','CSE',19),
	('2230','CSE',20),
	('2230','CSE',21),
	('2230','CSE',22),
	('2230','CSE',23),
	('2230','CSE',24),
	('2230','CSE',25),
	('2230','CSE',26),
	('2230','CSE',27),
	('2230','CSE',28),
	('2230','CSE',29),
	('2230','CSE',30),
	('2230','CSE',31),
	('2230','CSE',32),
	('2230','CSE',33),
	('2230','CSE',34),
	('2230','CSE',35),
	('2230','CSE',36),
	('2230','CSE',37),
	('2230','CSE',38),
	('2230','CSE',39),
	('2230','CSE',40),
	('2230','CSE',41),
	('2230','CSE',42),
	('2230','CSE',43),
	('2230','CSE',44),
	('2230','CSE',45),
	('2230','CSE',46),
	('2230','CSE',47),
	('2230','CSE',48),
	('2230','CSE',49),
	('2230','CSE',50),
	('2230','CSE',51),
	('2230','CSE',52),
	('2230','CSE',53),
	('2230','CSE',54),
	('2230','CSE',55),
	('2231','CSE',1),
	('2231','CSE',40),
	('3113','CSE',1),
	('3113','CSE',2),
	('3113','CSE',3),
	('3113','CSE',4),
	('3113','CSE',5),
	('3113','CSE',6),
	('3113','CSE',24),
	('3113','CSE',44),
	('3113','CSE',45),
	('3113','CSE',46),
	('3113','CSE',47),
	('3113','CSE',48),
	('3113','CSE',49),
	('3113','CSE',50),
	('3208','CSE',1),
	('3208','CSE',2),
	('3208','CSE',3),
	('3208','CSE',4),
	('3208','CSE',5),
	('3208','CSE',6),
	('3208','CSE',7),
	('3208','CSE',8),
	('3208','CSE',9),
	('3208','CSE',10),
	('3208','CSE',11),
	('3208','CSE',12),
	('3208','CSE',13),
	('3208','CSE',14),
	('3208','CSE',15),
	('3208','CSE',16),
	('3208','CSE',17),
	('3208','CSE',18),
	('3208','CSE',19),
	('3208','CSE',20),
	('3208','CSE',21),
	('3208','CSE',22),
	('3208','CSE',23),
	('3208','CSE',24),
	('3208','CSE',25),
	('3208','CSE',26),
	('3208','CSE',27),
	('3208','CSE',28),
	('3208','CSE',29),
	('3208','CSE',30),
	('3208','CSE',31),
	('3208','CSE',32),
	('3208','CSE',33),
	('3208','CSE',34),
	('3208','CSE',35),
	('3208','CSE',36),
	('3208','CSE',37),
	('3208','CSE',38),
	('3208','CSE',39),
	('3208','CSE',40),
	('3208','CSE',41),
	('3208','CSE',42),
	('3208','CSE',43),
	('3208','CSE',44),
	('3208','CSE',45),
	('3208','CSE',46),
	('3208','CSE',47),
	('3208','CSE',48),
	('3208','CSE',49),
	('3208','CSE',50),
	('3208','CSE',51),
	('3208','CSE',52),
	('3208','CSE',53),
	('3208','CSE',54),
	('3208','CSE',55);

/*!40000 ALTER TABLE `users_rooms` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
