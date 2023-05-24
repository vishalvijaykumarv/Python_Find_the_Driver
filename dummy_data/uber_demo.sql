-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 172.22.0.10:3306
-- Generation Time: May 24, 2023 at 06:17 AM
-- Server version: 8.0.33
-- PHP Version: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uber_demo`
--

-- --------------------------------------------------------

--
-- Table structure for table `driver_data`
--

CREATE TABLE `driver_data` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `current_latitude` varchar(20) NOT NULL,
  `current_longitude` varchar(20) NOT NULL,
  `on_ride` tinyint(1) NOT NULL,
  `price_km` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `driver_data`
--

INSERT INTO `driver_data` (`id`, `name`, `current_latitude`, `current_longitude`, `on_ride`, `price_km`) VALUES
(1, 'John', '40.7181', '-73.9647', 0, 15.5),
(2, 'Jane', '40.7395', '-74.0021', 0, 12.75),
(3, 'Mike', '40.7442', '-73.9912', 0, 11.25),
(4, 'Emily', '40.7489', '-73.9680', 1, 18.2),
(5, 'David', '40.7644', '-73.9857', 0, 16.8),
(6, 'Sarah', '40.6979', '-74.0369', 0, 13.4),
(7, 'Robert', '40.7614', '-73.9776', 0, 14.3),
(8, 'Michelle', '40.6979', '-74.0369', 0, 10.6),
(9, 'Christopher', '40.7395', '-73.9887', 1, 19.1),
(10, 'Olivia', '40.7527', '-73.9772', 0, 17.9);

-- --------------------------------------------------------

--
-- Table structure for table `user_rides`
--

CREATE TABLE `user_rides` (
  `id` int NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `requested_time` datetime(6) NOT NULL,
  `pickup_latitude` varchar(50) NOT NULL,
  `pickup_longitude` varchar(50) NOT NULL,
  `pickup_address` varchar(100) NOT NULL,
  `dropoff_latitude` varchar(50) NOT NULL,
  `dropoff_longitude` varchar(50) NOT NULL,
  `dropoff_address` varchar(100) NOT NULL,
  `estimated_duration` time(6) NOT NULL,
  `on_ride` tinyint(1) NOT NULL,
  `driver_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `user_rides`
--

INSERT INTO `user_rides` (`id`, `user_name`, `requested_time`, `pickup_latitude`, `pickup_longitude`, `pickup_address`, `dropoff_latitude`, `dropoff_longitude`, `dropoff_address`, `estimated_duration`, `on_ride`, `driver_name`) VALUES
(1, 'Alice Johnson', '2023-05-24 11:37:21.520000', '40.7128', '-74.0060', '123 Main St', '40.7489', '-73.9680', '456 Elm St', '00:06:00.000000', 1, 'Emily'),
(2, 'Bob Smith', '2023-05-24 11:37:21.524000', '40.7306', '-73.9352', '789 Oak Ave', '40.6979', '-74.0369', '321 Pine St', '00:08:00.000000', 1, 'Sarah'),
(3, 'Eva Davis', '2023-05-24 11:37:21.529000', '40.7223', '-73.9878', '987 Maple Rd', '40.7395', '-73.9887', '654 Birch Ln', '00:10:00.000000', 1, 'Christopher'),
(4, 'Mark Thompson', '2023-05-24 11:37:21.532000', '40.7614', '-73.9776', '654 Elm St', '40.7527', '-73.9772', '987 Maple Rd', '00:10:00.000000', 1, 'Olivia'),
(5, 'Lily Wilson', '2023-05-24 11:37:21.536000', '40.7527', '-73.9772', '321 Pine St', '40.7644', '-73.9857', '789 Oak Ave', '00:06:00.000000', 1, 'David'),
(6, 'Tom Anderson', '2023-05-24 11:37:21.541000', '40.7489', '-73.9680', '456 Elm St', '40.7306', '-73.9352', '123 Main St', '00:05:00.000000', 1, 'Emily'),
(7, 'Oliver Miller', '2023-05-24 11:37:21.544000', '40.7644', '-73.9857', '789 Oak Ave', '40.7614', '-73.9776', '654 Elm St', '00:05:00.000000', 1, 'Robert'),
(8, 'Sophia White', '2023-05-24 11:37:21.548000', '40.7395', '-73.9887', '654 Birch Ln', '40.7223', '-73.9878', '987 Maple Rd', '00:05:00.000000', 1, 'Christopher'),
(9, 'Emma Wilson', '2023-05-24 11:37:21.553000', '40.6979', '-74.0369', '321 Pine St', '40.7128', '-74.0060', '123 Main St', '00:10:00.000000', 0, NULL),
(10, 'Henry Taylor', '2023-05-24 11:37:21.556000', '40.7527', '-73.9772', '987 Maple Rd', '40.7306', '-73.9352', '789 Oak Ave', '00:10:00.000000', 0, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `driver_data`
--
ALTER TABLE `driver_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_rides`
--
ALTER TABLE `user_rides`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `driver_data`
--
ALTER TABLE `driver_data`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user_rides`
--
ALTER TABLE `user_rides`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
