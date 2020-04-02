-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 02, 2020 at 02:55 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sglovelah_chat`
--

-- --------------------------------------------------------

--
-- Table structure for table `chatdetails`
--

DROP TABLE IF EXISTS `chatdetails`;
CREATE TABLE IF NOT EXISTS `chatdetails` (
  `matchID` int(50) NOT NULL,
  `chatroom_ID` int(50) NOT NULL,
  PRIMARY KEY (`matchID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `chatdetails`
--

INSERT INTO `chatdetails` (`matchID`, `chatroom_ID`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `chatroom1`
--

DROP TABLE IF EXISTS `chatroom1`;
CREATE TABLE IF NOT EXISTS `chatroom1` (
  `messageID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(50) NOT NULL,
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msg` varchar(500) NOT NULL,
  PRIMARY KEY (`messageID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `chatroom1`
--

INSERT INTO `chatroom1` (`messageID`, `userID`, `created_on`, `msg`) VALUES
(1, 1, '2020-04-01 22:55:13', 'Hello!');

-- --------------------------------------------------------

--
-- Table structure for table `chatroom2`
--

DROP TABLE IF EXISTS `chatroom2`;
CREATE TABLE IF NOT EXISTS `chatroom2` (
  `messageID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(50) NOT NULL,
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msg` varchar(500) NOT NULL,
  PRIMARY KEY (`messageID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `chatroom3`
--

DROP TABLE IF EXISTS `chatroom3`;
CREATE TABLE IF NOT EXISTS `chatroom3` (
  `messageID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(50) NOT NULL,
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msg` varchar(500) NOT NULL,
  PRIMARY KEY (`messageID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `chatroom4`
--

DROP TABLE IF EXISTS `chatroom4`;
CREATE TABLE IF NOT EXISTS `chatroom4` (
  `messageID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(50) NOT NULL,
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msg` varchar(500) NOT NULL,
  PRIMARY KEY (`messageID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `chatroom5`
--

DROP TABLE IF EXISTS `chatroom5`;
CREATE TABLE IF NOT EXISTS `chatroom5` (
  `messageID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(50) NOT NULL,
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msg` varchar(500) NOT NULL,
  PRIMARY KEY (`messageID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `chatroom_details`
--

DROP TABLE IF EXISTS `chatroom_details`;
CREATE TABLE IF NOT EXISTS `chatroom_details` (
  `chatroom_ID` int(50) NOT NULL,
  `chatroom_name` varchar(50) NOT NULL,
  `serveraddress` varchar(50) NOT NULL,
  `Used` tinyint(1) NOT NULL,
  PRIMARY KEY (`chatroom_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `chatroom_details`
--

INSERT INTO `chatroom_details` (`chatroom_ID`, `chatroom_name`, `serveraddress`, `Used`) VALUES
(1, 'chatroom1', 'http://127.0.0.1:8001', 1),
(2, 'chatroom2', 'http://127.0.0.1:8002', 0),
(3, 'chatroom3', 'http://127.0.0.1:8003', 0),
(4, 'chatroom4', 'http://127.0.0.1:8004', 0),
(5, 'chatroom5', 'http://127.0.0.1:8005', 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
