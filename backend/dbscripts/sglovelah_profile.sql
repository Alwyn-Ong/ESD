-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 01, 2020 at 03:05 PM
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
  `name` varchar(50) NOT NULL,
  `bio` varchar(2083) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `age` int(3) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`profileID`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `profiledetails`
--

INSERT INTO `profiledetails` (`profileID`, `name`, `bio`, `gender`, `age`, `location`) VALUES
(1, 'Clement Sim', 'Happy wife, happy life!', 'M', 23, 'Tampines'),
(2, 'Kelsey Lim', 'Moomoo, I am a cow!', 'F', 22, 'Jurong East'),
(3, 'Jessica Liu', 'Here to make friends!', 'F', 21, 'Bugis'),
(4, 'Kaela Sim', 'Here for a supper friend!', 'F', 20, 'Changi'),
(5, 'Amanda Tan', 'Need a text buddy, look no more.', 'F', 24, 'West Coast'),
(6, 'Alichel Wong', 'I look better with a few more pounds!', 'F', 23, 'Bukit Batok');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
