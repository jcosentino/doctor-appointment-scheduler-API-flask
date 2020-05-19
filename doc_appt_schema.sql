CREATE DATABASE  IF NOT EXISTS `doc_appt_schema` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `doc_appt_schema`;
-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: doc_appt_schema
-- ------------------------------------------------------
-- Server version	5.7.29-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `appointmentid` int(11) NOT NULL AUTO_INCREMENT,
  `apptTime` datetime DEFAULT NULL,
  `available` tinyint(1) NOT NULL,
  `createdDate` datetime NOT NULL,
  `lastUpdated` datetime NOT NULL,
  PRIMARY KEY (`appointmentid`),
  UNIQUE KEY `apptTime` (`apptTime`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,'2005-01-09 10:32:18',1,'2020-05-19 19:32:53','2020-05-19 19:32:53');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insurance`
--

DROP TABLE IF EXISTS `insurance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insurance` (
  `insuranceid` int(11) NOT NULL AUTO_INCREMENT,
  `insurancecompany` varchar(80) NOT NULL,
  `groupnumber` varchar(16) NOT NULL,
  `memberid` varchar(16) NOT NULL,
  `createdDate` datetime NOT NULL,
  `lastUpdated` datetime NOT NULL,
  PRIMARY KEY (`insuranceid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insurance`
--

LOCK TABLES `insurance` WRITE;
/*!40000 ALTER TABLE `insurance` DISABLE KEYS */;
INSERT INTO `insurance` VALUES (1,'Nowhere LLC','234000','5012332312','2020-05-19 19:32:57','2020-05-19 19:32:57');
/*!40000 ALTER TABLE `insurance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile` (
  `profileid` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(80) DEFAULT NULL,
  `lastname` varchar(80) DEFAULT NULL,
  `ssn` varchar(9) DEFAULT NULL,
  `phonenumber` varchar(10) DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `createdDate` datetime DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `userid` int(11) NOT NULL,
  `insuranceid` int(11) DEFAULT NULL,
  `appointmentid` int(11) DEFAULT NULL,
  PRIMARY KEY (`profileid`),
  KEY `userid` (`userid`),
  KEY `insuranceid` (`insuranceid`),
  KEY `appointmentid` (`appointmentid`),
  CONSTRAINT `profile_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`),
  CONSTRAINT `profile_ibfk_2` FOREIGN KEY (`insuranceid`) REFERENCES `insurance` (`insuranceid`),
  CONSTRAINT `profile_ibfk_3` FOREIGN KEY (`appointmentid`) REFERENCES `appointment` (`appointmentid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile`
--

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
INSERT INTO `profile` VALUES (1,'First','Last','123456789','7181231234','2005-01-09 10:32:18','2020-05-19 19:32:34','2020-05-19 19:33:00',1,1,1),(2,NULL,NULL,NULL,NULL,NULL,'2020-05-19 19:33:09','2020-05-19 19:33:09',2,NULL,NULL);
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(80) NOT NULL,
  `password` varchar(512) NOT NULL,
  `createdDate` datetime NOT NULL,
  `lastUpdated` datetime NOT NULL,
  `isadmin` tinyint(1) NOT NULL,
  `sec_ques_num` int(11) NOT NULL,
  `sec_ques_ans` varchar(512) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'example@example.com','sha256$uGXeyQuw$bc599ae6889083f2267b9588ff31075c614c84e2875c14d3de3862a378e0a816','2020-05-19 19:32:34','2020-05-19 19:32:34',0,1,'sha256$4p26BtcH$503e91c932d0552039fd47e28dabef8fa28db31bb776e0c6562439f6ad36b8a0'),(2,'admin@example.com','sha256$KM8ewK6l$dc36d0f362bfdb03e09bac0fd4d867b9662d8a9de72d9ed87326996394b18a64','2020-05-19 19:33:09','2020-05-19 19:33:09',1,1,'sha256$qa6yZFc1$6db52dbec099278a01537c7607d2cd72c88b518de3247b8d5c990e5991652f21');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-19 19:33:52
