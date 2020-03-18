-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 18, 2020 at 06:08 AM
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
-- Database: `sglovelah_profile`
--

-- --------------------------------------------------------

--
-- Table structure for table `profiledetails`
--

DROP TABLE IF EXISTS `profiledetails`;
CREATE TABLE IF NOT EXISTS `profiledetails` (
  `profileID` int(255) NOT NULL AUTO_INCREMENT,
  `bio` varchar(2083) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `age` int(3) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`profileID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `profiledetails`
--

INSERT INTO `profiledetails` (`profileID`, `bio`, `gender`, `age`, `location`) VALUES
(1, 'hello i am so handsome', 'M', 25, 'Bedok'),
(2, 'HELLO i am so pretty!', 'F', 9, 'Jurong'),
(5, 'hey updated noobs', 'F', 5, 'updated loc too'),
(11, 'testing #1', 'F', 21, 'testing update');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
