-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: uqi_capstone1
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `nilai_siswa`
--

DROP TABLE IF EXISTS `nilai_siswa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nilai_siswa` (
  `nis` varchar(20) NOT NULL,
  `nama_siswa` varchar(100) DEFAULT NULL,
  `jenis_kelamin` char(1) DEFAULT NULL,
  `kelas` varchar(10) DEFAULT NULL,
  `nilai_matematika` int DEFAULT NULL,
  `nilai_fisika` int DEFAULT NULL,
  `nilai_kimia` int DEFAULT NULL,
  `nilai_biologi` int DEFAULT NULL,
  `nilai_english` int DEFAULT NULL,
  `nilai_bahasa_indonesia` int DEFAULT NULL,
  PRIMARY KEY (`nis`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nilai_siswa`
--

LOCK TABLES `nilai_siswa` WRITE;
/*!40000 ALTER TABLE `nilai_siswa` DISABLE KEYS */;
INSERT INTO `nilai_siswa` VALUES ('241001','Uqi Shafi','L','XI A',98,95,90,92,90,92),('241002','Bunga Citra Lestari','P','XI B',75,80,72,78,85,88),('241003','Candra Wijaya Kusuma','L','XI A',90,92,88,85,70,80),('241004','Dinda Kirana Putri','P','XI C',65,70,68,75,80,85),('241005','Eko Wahyu Saputra','L','XI D',88,85,90,88,75,78),('241006','Fajar Siddiq','L','XI B',70,65,70,72,60,75),('241007','Gilang Ramadhan','L','XI A',95,90,92,90,85,82),('241008','Hana Kartika Sari','P','XI C',80,82,80,85,90,92),('241009','Indah Permata Sari','P','XI D',78,75,76,80,88,90),('241010','Joko Susilo','L','XI B',60,65,62,68,70,75),('241011','Kartika Dewi','P','XI A',82,80,85,88,92,95),('241012','Lukman Hakim','L','XI C',75,70,72,75,78,80),('241013','Muhammad Rizky','L','XI D',85,88,85,82,80,85),('241014','Nadia Utami','P','XI A',90,95,90,92,98,90),('241015','Oscar Mahendra','L','XI B',65,60,65,70,72,75),('241016','Putri Ayu Wardani','P','XI C',88,85,82,88,90,92),('241017','Qory Sandioriva','P','XI D',72,75,70,78,80,82),('241018','Rian Hidayat','L','XI A',80,82,85,80,75,78),('241019','Siti Aminah','P','XI B',92,88,90,95,85,88),('241020','Taufik Hidayat','L','XI C',70,72,68,75,70,75),('241021','Umar Wirahadikusumah','L','XI D',85,80,82,85,88,90),('241022','Vina Panduwinata','P','XI A',78,75,80,82,85,88),('241023','Wahyu Nugroho','L','XI B',65,68,70,72,75,80),('241024','Xavier Alexander','L','XI C',90,92,95,90,88,85),('241025','Yusuf Mansur','L','XI D',82,85,80,88,90,92),('241026','Zahra Nabila','P','XI A',95,98,92,95,90,92),('241027','Agus Setiawan','L','XI B',60,62,65,68,70,72),('241028','Bella Saphira','P','XI C',75,78,80,82,85,88),('241029','Choky Sitohang','L','XI D',88,90,85,88,82,85),('241030','Dewi Sandra','P','XI A',92,90,88,92,95,90),('241031','Erick Thohir','L','XI B',80,82,85,80,78,80),('241032','Farah Quinn','P','XI C',70,75,72,78,80,85),('241033','Gading Marten','L','XI D',85,80,82,85,88,90),('241034','Hesti Purwadinata','P','XI A',78,75,70,75,80,82),('241035','Irfan Hakim','L','XI B',65,70,68,72,75,78),('241036','Jessica Iskandar','P','XI C',90,88,92,90,85,88),('241037','Kevin Julio','L','XI D',82,85,80,88,90,92),('241038','Luna Maya','P','XI A',95,92,90,95,98,95),('241039','Marcel Chandrawinata','L','XI B',75,78,72,75,80,82),('241040','Nikita Willy','P','XI C',88,85,90,88,92,90),('241041','Oki Setiana Dewi','P','XI D',92,95,90,92,90,88),('241042','Prilly Latuconsina','P','XI A',80,82,85,88,90,92),('241043','Raffi Ahmad','L','XI B',70,72,75,78,80,85),('241044','Syahrini Fatimah','P','XI C',65,68,70,72,75,78),('241045','Titi Kamal','P','XI D',85,88,90,85,82,85),('241046','Uya Kuya','L','XI A',78,80,82,85,88,90),('241047','Vino G Bastian','L','XI B',90,92,95,90,85,88),('241048','Wulan Guritno','P','XI C',82,80,78,85,88,90),('241049','Yuki Kato','P','XI D',75,78,80,82,85,88),('241050','Zaskia Sungkar','P','XI A',88,90,92,95,90,92),('241051','Shafi Uqi','L','XI C',95,100,100,100,100,100),('241052','Riska Puspita','P','XI B',54,76,87,83,76,96),('241053','Uqi Uqian','L','XI D',100,100,95,100,100,100);
/*!40000 ALTER TABLE `nilai_siswa` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-28  0:16:41
