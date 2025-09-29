-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 29, 2025 at 06:00 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `healthmate`
--

-- --------------------------------------------------------

--
-- Table structure for table `analyzed_reports`
--

DROP TABLE IF EXISTS `analyzed_reports`;
CREATE TABLE IF NOT EXISTS `analyzed_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `original_text` text,
  `explanation` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `diagnoses`
--

DROP TABLE IF EXISTS `diagnoses`;
CREATE TABLE IF NOT EXISTS `diagnoses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `symptoms` varchar(255) DEFAULT NULL,
  `treatment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `diseases`
--

DROP TABLE IF EXISTS `diseases`;
CREATE TABLE IF NOT EXISTS `diseases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fcm_tokens`
--

DROP TABLE IF EXISTS `fcm_tokens`;
CREATE TABLE IF NOT EXISTS `fcm_tokens` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `token` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `fcm_tokens`
--

INSERT INTO `fcm_tokens` (`id`, `user_id`, `token`, `created_at`) VALUES
(2, 4, 'fRC8YWRekjSl9K1vPuI_Z9:APA91bG5QwRg-jg0rKSsgTHNS1JXvpG5963im0khgjcRw3vMu95IX-Lgf18-yqvHrl0vg5Tp2GtulQx1Cyw5KtVI_ZkBPtwea4_v3KiGMb1m8UiB2w9nIfE', '2025-05-09 21:37:03'),
(3, 1, 'd_pSZ6cWB0IyP2syzQxMI0:APA91bHl3dCiZzZVRh51iiC4Ob-pS36KTWr6fkwFnRomIVjWK-_B_0sTE9FExe2729aRC8pzLH0x2DoN6ritnwkb60rav-KWgZjBkWGnUTul04Wr2WCPR4Y', '2025-05-09 22:15:53');

-- --------------------------------------------------------

--
-- Table structure for table `health_reports`
--

DROP TABLE IF EXISTS `health_reports`;
CREATE TABLE IF NOT EXISTS `health_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `predicted_disease` varchar(100) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `description` text,
  `symptoms` text,
  `precautions` text,
  `medications` text,
  `diets` text,
  `workouts` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `health_reports`
--

INSERT INTO `health_reports` (`id`, `user_id`, `name`, `gender`, `age`, `predicted_disease`, `confidence`, `description`, `symptoms`, `precautions`, `medications`, `diets`, `workouts`, `created_at`) VALUES
(16, 4, 'Prashant Senapati', 'Male', 53, 'Gastroenteritis', 0.45, 'Gastroenteritis is an inflammation of the stomach and intestines, typically caused by a virus or bacteria.', '[\"weight_loss\", \"sunken_eyes\"]', '[]', '[\"[\'Metronidazole\', \'Ondansetron\', \'Bismuth subsalicylate\', \'Ringer\'s Lactate\', \'Lactobacillus rhamnosus GG \']\"]', '[\"[\'Bland Diet\', \'Bananas\', \'Rice\', \'Applesauce\', \'Toast\']\"]', '[\"Stay hydrated\", \"Consume clear fluids\", \"Follow the BRAT diet (bananas, rice, applesauce, toast)\", \"Include bland foods\", \"Avoid fatty and greasy foods\", \"Limit caffeine and alcohol\", \"Avoid spicy foods\", \"Consult a healthcare professional\", \"Gradually reintroduce solid foods\", \"Avoid dairy products\"]', '2025-06-24 04:50:54'),
(17, 4, 'Biswajit', 'Male', 21, 'GERD', 0.42, 'GERD (Gastroesophageal Reflux Disease) is a digestive disorder that affects the lower esophageal sphincter.', '[\"acidity\", \"stomach_pain\"]', '[\"avoid fatty spicy food               \", \"avoid lying down after eating      \", \"maintain healthy weight                \", \"exercise\"]', '[\"[\'Prilosec\', \'Omeprazole capsules\', \'Mylanta, Rolaids\', \'Domperidone\', \'Pantoprazole\']\"]', '[\"[\'Low-Acid Diet\', \'Fiber-rich foods\', \'Ginger\', \'Licorice\', \'Aloe vera juice\']\"]', '[\"Consume smaller meals\", \"Avoid trigger foods (spicy, fatty)\", \"Eat high-fiber foods\", \"Limit caffeine and alcohol\", \"Chew food thoroughly\", \"Avoid late-night eating\", \"Consume non-citrus fruits\", \"Include lean proteins\", \"Stay hydrated\", \"Avoid carbonated beverages\"]', '2025-09-05 05:33:31'),
(10, 4, 'Biswajit Senapati', 'Male', 21, 'Paralysis (brain hemorrhage)', 0.2, 'Paralysis (brain hemorrhage) refers to the loss of muscle function due to bleeding in the brain.', '[\"vomiting\", \"mood_swings\"]', '[\"massage                              \", \"eat healthy                        \", \"exercise                               \", \"consult doctor\"]', '[\"Warfarin \", \"Alteplase (Activase) or Tenecteplase (TNKase)\", \"Levetiracetam and Phenytoin\", \"Physical therapy\", \"Occupational therapy\"]', '[\"Heart-Healthy Diet\", \"Low-sodium foods\", \"Fruits and vegetables\", \"Whole grains\", \"Lean proteins\"]', '[\"Follow a balanced and nutritious diet\", \"Include lean proteins\", \"Consume nutrient-rich foods\", \"Stay hydrated\", \"Include healthy fats\", \"Limit sugary foods and beverages\", \"Include antioxidants\", \"Consume foods rich in vitamin K\", \"Consult a healthcare professional\", \"Manage stress\"]', '2025-05-07 09:11:53'),
(12, 1, 'Biswajit', 'Male', 21, 'Cervical spondylosis', 0.36, 'Cervical spondylosis is a degenerative condition of the cervical spine.', '[\"back_pain\", \"mild_fever\"]', '[\"use heating pad or cold pack         \", \"exercise                           \", \"take otc pain reliver                  \", \"consult doctor\"]', '[\"Naproxen\", \"Spasdilite EP\", \"Physical therapy\", \"Neck braces\", \"Prednisone or Methylprednisolone\"]', '[\"Arthritis Diet\", \"Anti-Inflammatory Diet\", \"Omega-3-rich foods\", \"Fruits and vegetables\", \"Whole grains\"]', '[\"Include anti-inflammatory foods\", \"Consume omega-3 fatty acids\", \"Include vitamin D-rich foods\", \"Stay hydrated\", \"Consume antioxidant-rich foods\", \"Limit processed foods\", \"Include lean proteins\", \"Practice good posture\", \"Consult a healthcare professional\", \"Engage in regular exercise\"]', '2025-05-10 04:59:03'),
(13, 1, 'Avhi', 'Male', 21, 'Hypertension ', 0.22, 'No description available.', '[\"loss_of_balance\", \"mood_swings\"]', '[]', '[]', '[]', '[]', '2025-05-10 05:00:53'),
(14, 1, 'biswa', 'Male', 21, 'Cervical spondylosis', 0.33, 'Cervical spondylosis is a degenerative condition of the cervical spine.', '[\"back_pain\", \"headache\"]', '[\"use heating pad or cold pack         \", \"exercise                           \", \"take otc pain reliver                  \", \"consult doctor\"]', '[\"Naproxen\", \"Spasdilite EP\", \"Physical therapy\", \"Neck braces\", \"Prednisone or Methylprednisolone\"]', '[\"Arthritis Diet\", \"Anti-Inflammatory Diet\", \"Omega-3-rich foods\", \"Fruits and vegetables\", \"Whole grains\"]', '[\"Include anti-inflammatory foods\", \"Consume omega-3 fatty acids\", \"Include vitamin D-rich foods\", \"Stay hydrated\", \"Consume antioxidant-rich foods\", \"Limit processed foods\", \"Include lean proteins\", \"Practice good posture\", \"Consult a healthcare professional\", \"Engage in regular exercise\"]', '2025-05-10 05:02:00'),
(15, 1, 'Aditya', 'Male', 21, 'Allergy', 0.24, 'Allergy is an immune system reaction to a substance in the environment.', '[\"mild_fever\", \"cold_hands_and_feets\", \"continuous_sneezing\", \"cough\"]', '[\"apply calamine                       \", \"cover area with bandage            \", \"                                       \", \"use ice to compress itching\"]', '[\" Allergy Relief Antihistamines Tablet\", \"Sudafed PE or Afrin\", \"Epinephrine injection\", \"Corticosteroids\", \"Immunotherapy\"]', '[\"Elimination Diet\", \"Omega-3-rich foods\", \"Vitamin C-rich foods\", \"Quercetin-rich foods\", \"Probiotics\"]', '[\"Avoid allergenic foods\", \"Consume anti-inflammatory foods\", \"Include omega-3 fatty acids\", \"Stay hydrated\", \"Eat foods rich in vitamin C\", \"Include quercetin-rich foods\", \"Consume local honey\", \"Limit processed foods\", \"Include ginger in diet\", \"Avoid artificial additives\"]', '2025-05-10 05:03:19'),
(7, 4, 'Biswajit', 'Male', 21, 'Allergy', 0.24, 'Allergy is an immune system reaction to a substance in the environment.', '[\"cough\", \"cold_hands_and_feets\", \"mild_fever\", \"continuous_sneezing\"]', '[\"apply calamine                       \", \"cover area with bandage            \", \"                                       \", \"use ice to compress itching\"]', '[\" Allergy Relief Antihistamines Tablet\", \"Sudafed PE or Afrin\", \"Epinephrine injection\", \"Corticosteroids\", \"Immunotherapy\"]', '[\"Elimination Diet\", \"Omega-3-rich foods\", \"Vitamin C-rich foods\", \"Quercetin-rich foods\", \"Probiotics\"]', '[\"Avoid allergenic foods\", \"Consume anti-inflammatory foods\", \"Include omega-3 fatty acids\", \"Stay hydrated\", \"Eat foods rich in vitamin C\", \"Include quercetin-rich foods\", \"Consume local honey\", \"Limit processed foods\", \"Include ginger in diet\", \"Avoid artificial additives\"]', '2025-05-07 06:02:27'),
(8, 4, 'biswa', 'Male', 21, 'GERD', 0.31, 'GERD (Gastroesophageal Reflux Disease) is a digestive disorder that affects the lower esophageal sphincter.', '[\"ulcers_on_tongue\", \"fatigue\"]', '[\"avoid fatty spicy food               \", \"avoid lying down after eating      \", \"maintain healthy weight                \", \"exercise\"]', '[\"Prilosec\", \"Omeprazole capsules\", \"Mylanta, Rolaids\", \"Domperidone\", \"Pantoprazole\"]', '[\"Low-Acid Diet\", \"Fiber-rich foods\", \"Ginger\", \"Licorice\", \"Aloe vera juice\"]', '[\"Consume smaller meals\", \"Avoid trigger foods (spicy, fatty)\", \"Eat high-fiber foods\", \"Limit caffeine and alcohol\", \"Chew food thoroughly\", \"Avoid late-night eating\", \"Consume non-citrus fruits\", \"Include lean proteins\", \"Stay hydrated\", \"Avoid carbonated beverages\"]', '2025-05-07 06:46:58'),
(18, 4, 'Biswajit', 'Male', 21, 'GERD', 0.42, 'GERD (Gastroesophageal Reflux Disease) is a digestive disorder that affects the lower esophageal sphincter.', '[\"acidity\", \"stomach_pain\"]', '[\"avoid fatty spicy food               \", \"avoid lying down after eating      \", \"maintain healthy weight                \", \"exercise\"]', '[\"[\'Prilosec\', \'Omeprazole capsules\', \'Mylanta, Rolaids\', \'Domperidone\', \'Pantoprazole\']\"]', '[\"[\'Low-Acid Diet\', \'Fiber-rich foods\', \'Ginger\', \'Licorice\', \'Aloe vera juice\']\"]', '[\"Consume smaller meals\", \"Avoid trigger foods (spicy, fatty)\", \"Eat high-fiber foods\", \"Limit caffeine and alcohol\", \"Chew food thoroughly\", \"Avoid late-night eating\", \"Consume non-citrus fruits\", \"Include lean proteins\", \"Stay hydrated\", \"Avoid carbonated beverages\"]', '2025-09-05 05:33:36'),
(19, 4, 'Amrendra', 'Male', 31, 'Allergy', 0.44, 'Allergy is an immune system reaction to a substance in the environment.', '[\"shivering\", \"vomiting\", \"fatigue\", \"weight_gain\"]', '[\"apply calamine                       \", \"cover area with bandage            \", \"                                       \", \"use ice to compress itching\"]', '[\"[\' Allergy Relief Antihistamines Tablet\', \'Sudafed PE or Afrin\', \'Epinephrine injection\', \'Corticosteroids\', \'Immunotherapy\']\"]', '[\"[\'Elimination Diet\', \'Omega-3-rich foods\', \'Vitamin C-rich foods\', \'Quercetin-rich foods\', \'Probiotics\']\"]', '[\"Avoid allergenic foods\", \"Consume anti-inflammatory foods\", \"Include omega-3 fatty acids\", \"Stay hydrated\", \"Eat foods rich in vitamin C\", \"Include quercetin-rich foods\", \"Consume local honey\", \"Limit processed foods\", \"Include ginger in diet\", \"Avoid artificial additives\"]', '2025-09-05 05:48:49'),
(20, 4, 'Amrendra', 'Male', 31, 'Allergy', 0.44, 'Allergy is an immune system reaction to a substance in the environment.', '[\"shivering\", \"vomiting\", \"fatigue\", \"weight_gain\"]', '[\"apply calamine                       \", \"cover area with bandage            \", \"                                       \", \"use ice to compress itching\"]', '[\"[\' Allergy Relief Antihistamines Tablet\', \'Sudafed PE or Afrin\', \'Epinephrine injection\', \'Corticosteroids\', \'Immunotherapy\']\"]', '[\"[\'Elimination Diet\', \'Omega-3-rich foods\', \'Vitamin C-rich foods\', \'Quercetin-rich foods\', \'Probiotics\']\"]', '[\"Avoid allergenic foods\", \"Consume anti-inflammatory foods\", \"Include omega-3 fatty acids\", \"Stay hydrated\", \"Eat foods rich in vitamin C\", \"Include quercetin-rich foods\", \"Consume local honey\", \"Limit processed foods\", \"Include ginger in diet\", \"Avoid artificial additives\"]', '2025-09-05 05:49:03'),
(21, 4, 'Biswajit Senapati', 'Male', 21, 'Fungal Infection', 0.77, 'Infection caused by fungi affecting skin, nails, or systemic organs.', '[\"Itching\", \"Burning_Sensation\"]', '[\"Keep affected area dry\", \"avoid sharing personal items.\"]', '[\"Topical antifungals (clotrimazole\", \"ketoconazole)\", \"oral (fluconazole) if systemic.\"]', '[\"Avoid sugar\", \"refined carbs\", \"include probiotics and protein-rich foods.\"]', '[\"Light activity; avoid excessive sweating on affected areas.\"]', '2025-09-29 10:17:20'),
(22, 4, 'pappu', 'Male', 23, 'Fungal Infection', 0.77, 'Infection caused by fungi affecting skin, nails, or systemic organs.', '[\"Itching\", \"Burning_Sensation\"]', '[\"Keep affected area dry\", \"avoid sharing personal items.\"]', '[\"Topical antifungals (clotrimazole\", \"ketoconazole)\", \"oral (fluconazole) if systemic.\"]', '[\"Avoid sugar\", \"refined carbs\", \"include probiotics and protein-rich foods.\"]', '[\"Light activity; avoid excessive sweating on affected areas.\"]', '2025-09-29 11:08:09'),
(23, 4, 'Pappu ', 'Male', 23, NULL, 16.15, 'No description available.', '[\"Chest_Pain\", \"Vomiting\"]', '[]', '[]', '[]', '[]', '2025-09-29 11:16:05'),
(24, 4, 'papu', 'Male', 23, 'GERD', 0.16, 'Acid reflux causing heartburn.', '[\"Vomiting\", \"Chest_Pain\"]', '[\"Avoid lying down after meals\", \"maintain healthy weight.\"]', '[\"Antacids\", \"PPIs\", \"H2 blockers.\"]', '[\"Small\", \"frequent meals\", \"avoid spicy\", \"fatty foods\", \"hydration.\"]', '[\"Light aerobic activity; avoid exercises that increase abdominal pressure.\"]', '2025-09-29 11:22:24'),
(25, 4, 'pappu', 'Male', 21, 'High Blood Pressure', 0.13, 'Chronic elevated blood pressure.', '[\"Chest_Pain\", \"Fever\"]', '[\"Monitor BP\", \"maintain healthy weight\", \"limit alcohol.\"]', '[\"ACE inhibitors\", \"ARBs\", \"beta-blockers\", \"diuretics.\"]', '[\"DASH diet\", \"low-sodium\", \"fruits and vegetables.\"]', '[\"Aerobic exercise; resistance training; avoid uncontrolled high-intensity exercise.\"]', '2025-09-29 11:23:26'),
(26, 4, 'Pappu Senapati', 'Male', 23, 'Diabetes', 0.21, 'Chronic metabolic disorder with high blood sugar.', '[\"Body_Pain\", \"Joint_Pain\", \"Fever\", \"Feel_Cold\", \"Cough\", \"Continuous_Sneezing\"]', '[\"Monitor blood sugar\", \"maintain weight\", \"foot care.\"]', '[\"Metformin\", \"sulfonylureas\", \"SGLT2 inhibitors\", \"insulin if needed.\"]', '[\"Low-GI foods\", \"high fiber\", \"lean protein\", \"limit sugar and refined carbs.\"]', '[\"Regular aerobic exercise\", \"resistance training; monitor glucose.\"]', '2025-09-29 11:48:28'),
(27, 4, 'Pappu Senapati', 'Male', 23, 'Diabetes', 0.21, 'Chronic metabolic disorder with high blood sugar.', '[\"Body_Pain\", \"Joint_Pain\", \"Fever\", \"Feel_Cold\", \"Cough\", \"Continuous_Sneezing\"]', '[\"Monitor blood sugar\", \"maintain weight\", \"foot care.\"]', '[\"Metformin\", \"sulfonylureas\", \"SGLT2 inhibitors\", \"insulin if needed.\"]', '[\"Low-GI foods\", \"high fiber\", \"lean protein\", \"limit sugar and refined carbs.\"]', '[\"Regular aerobic exercise\", \"resistance training; monitor glucose.\"]', '2025-09-29 11:48:45'),
(28, 4, 'raj', 'Male', 23, 'Ringworm', 0.86, 'Superficial fungal skin infection.', '[\"Itching\", \"Burning_Sensation\", \"Rash\"]', '[\"Keep skin dry\", \"avoid sharing personal items.\"]', '[\"Topical antifungals\", \"oral antifungals if widespread.\"]', '[\"Avoid sugar\", \"protein-rich diet\", \"probiotics.\"]', '[\"Light activity; avoid sweating on affected area.\"]', '2025-09-29 14:23:44'),
(29, 4, 'raj', 'Male', 23, 'Pleurisy', 0.73, 'Inflammation of lung lining causing chest pain', '[\"Chest_Pain\", \"Fever\"]', '[\"Avoid deep coughing\", \"rest.\"]', '[\"NSAIDs\", \"treat underlying infection.\"]', '[\"Hydration\", \"light\", \"nutrient-rich diet.\"]', '[\"Breathing exercises; light activity post-recovery.\"]', '2025-09-29 14:24:24'),
(30, 4, 'raj', 'Male', 23, 'CCHFV (Crimean Congo Hemorrhagic Fever)', 0.17, 'Crimean-Congo Hemorrhagic Fever, viral hemorrhagic fever.', '[\"Continuous_Sneezing\", \"Sore_Throat\", \"Feel_Cold\"]', '[\"Avoid contact with blood\", \"vector protection.\"]', '[\"Supportive care\", \"no specific antiviral.\"]', '[\"Hydration\", \"soft nutrient-rich foods.\"]', '[\"Rest during illness; light mobility post-recovery\"]', '2025-09-29 14:39:27'),
(31, 4, 'biswajit', 'Male', 23, 'GERD', 0.06, 'Acid reflux causing heartburn.', '[\"Chest_Pain\", \"Vomiting\"]', '[\"Avoid lying down after meals\", \"maintain healthy weight.\"]', '[\"Antacids\", \"PPIs\", \"H2 blockers.\"]', '[\"Small\", \"frequent meals\", \"avoid spicy\", \"fatty foods\", \"hydration.\"]', '[\"Light aerobic activity; avoid exercises that increase abdominal pressure.\"]', '2025-09-29 15:39:35'),
(32, 4, 'biswajit', 'Male', 23, 'GERD', 0.06, 'Acid reflux causing heartburn.', '[\"Chest_Pain\", \"Vomiting\"]', '[\"Avoid lying down after meals\", \"maintain healthy weight.\"]', '[\"Antacids\", \"PPIs\", \"H2 blockers.\"]', '[\"Small\", \"frequent meals\", \"avoid spicy\", \"fatty foods\", \"hydration.\"]', '[\"Light aerobic activity; avoid exercises that increase abdominal pressure.\"]', '2025-09-29 15:43:25');

-- --------------------------------------------------------

--
-- Table structure for table `medications`
--

DROP TABLE IF EXISTS `medications`;
CREATE TABLE IF NOT EXISTS `medications` (
  `medication_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `dosage` varchar(50) DEFAULT NULL,
  `frequency` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`medication_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `medication_reminders`
--

DROP TABLE IF EXISTS `medication_reminders`;
CREATE TABLE IF NOT EXISTS `medication_reminders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `medicine_name` varchar(255) NOT NULL,
  `dosage` varchar(255) NOT NULL,
  `reminder_times` text NOT NULL,
  `frequency` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `medication_reminders`
--

INSERT INTO `medication_reminders` (`id`, `user_id`, `medicine_name`, `dosage`, `reminder_times`, `frequency`, `start_date`, `end_date`, `created_at`) VALUES
(7, 4, 'Antacide', '10mg', '[\"03:16\"]', 'Daily', '2025-05-10', '2025-05-13', '2025-05-09 16:15:23'),
(6, 4, 'Antacid', '10mg', '[\"03:11\"]', 'Daily', '2025-05-10', '2025-05-13', '2025-05-09 16:09:28'),
(5, 4, 'Parax', '100mg', '[\"02:57\"]', 'Daily', '2025-05-10', '2025-05-12', '2025-05-09 15:56:48'),
(4, 4, 'Paramoll', '100mg', '[\"02:43\"]', 'Daily', '2025-05-10', '2025-05-11', '2025-05-09 15:42:18'),
(8, 4, 'antidode', '10mg', '[\"03:21\"]', 'Daily', '2025-05-10', '2025-05-11', '2025-05-09 16:19:53'),
(9, 4, 'Nase', '10mg', '[\"03:26\"]', 'Daily', '2025-05-10', '2025-05-11', '2025-05-09 16:25:18'),
(10, 4, 'Nase', '10mg', '[\"03:31\"]', 'Daily', '2025-05-10', '2025-05-11', '2025-05-09 16:30:12'),
(11, 1, 'paracetamol', '10mg', '[\"03:47\"]', 'Daily', '2025-05-10', '2025-05-11', '2025-05-09 16:46:37'),
(12, 1, 'Tramadol', '500mg', '[\"10:25\"]', 'Daily', '2025-05-10', '2025-05-11', '2025-05-09 23:24:20'),
(13, 4, 'Meltladose', '10mg', '[\"11:24\"]', 'Daily', '2025-05-10', '2025-05-11', '2025-05-10 00:22:53'),
(14, 4, 'Meltladose', '10mg', '[\"11:37\"]', 'Daily', '2025-05-10', '2025-05-10', '2025-05-10 00:36:37'),
(15, 4, 'hilo', '10mg', '[\"11:43\"]', 'Daily', '2025-05-10', '2025-05-10', '2025-05-10 00:43:10'),
(16, 4, 'Antacid', '100mg', '[\"11:52\"]', 'Daily', '2025-05-10', '2025-05-10', '2025-05-10 00:52:07'),
(17, 4, 'Antacid', '100mg', '[\"11:53\"]', 'Daily', '2025-05-10', '2025-05-10', '2025-05-10 00:52:32'),
(18, 1, 'Paracetamol', '500mg', '[\"18:53\"]', 'Daily', '2025-05-13', '2025-05-13', '2025-05-13 07:51:51'),
(19, 4, 'Abv', '100mg', '[\"19:49\"]', 'Daily', '2025-06-13', '2025-06-13', '2025-06-13 08:48:31'),
(20, 4, 'Quarine FG', '200mg', '[\"19:53\"]', 'Daily', '2025-06-13', '2025-06-13', '2025-06-13 08:52:20'),
(21, 4, 'Asprin z', '500mg', '[\"11:09\"]', 'Daily', '2025-06-24', '2025-06-24', '2025-06-24 00:08:38'),
(22, 4, 'AAAAAAAAA', '100mg', '[\"13:46\"]', 'Daily', '2025-07-17', '2025-07-17', '2025-07-17 02:46:03'),
(23, 4, 'AAAAAAAAA', '100mg', '[\"13:48\"]', 'Daily', '2025-07-17', '2025-07-17', '2025-07-17 02:47:37');

-- --------------------------------------------------------

--
-- Table structure for table `privacy_settings`
--

DROP TABLE IF EXISTS `privacy_settings`;
CREATE TABLE IF NOT EXISTS `privacy_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `share_data` tinyint(1) DEFAULT '1',
  `allow_emails` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reminder_history`
--

DROP TABLE IF EXISTS `reminder_history`;
CREATE TABLE IF NOT EXISTS `reminder_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reminder_id` int NOT NULL,
  `user_id` int NOT NULL,
  `medication_name` varchar(255) NOT NULL,
  `dosage` varchar(255) DEFAULT NULL,
  `timing` varchar(255) NOT NULL,
  `reminder_time` varchar(10) NOT NULL,
  `status` enum('Not Taken','Taken','Missed','Skipped') DEFAULT 'Not Taken',
  `notes` text,
  `taken_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `reminder_id` (`reminder_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `age`, `gender`, `password`, `is_admin`, `created_at`, `is_active`, `is_deleted`) VALUES
(1, 'Biswajit', 'user@gmail.com', 21, 'Male', 'scrypt:32768:8:1$6F5E4jdFhY3S0dWT$c7954a97b488b6b4a7d0b9df9cb009e7ae1103fd7f1f82af06e2ef7ec359615955ff6680bb201eb0090c3fd401cfe82b5e8a9255ccfc414d3f7c58be118d4122', 1, '2025-05-07 09:32:14', 1, 0),
(2, 'Vansh', 'vansh@gmail.com', 21, 'Male', 'scrypt:32768:8:1$FrxhIHm6ExXPCJ47$f25744fdb1167fc31152b6d18c9dfda45aeef0f6622d7bde98469ebc159c63599a19e96a2e2f207e550648c3ce6f04ba339e12930233829db62292d898668004', 0, '2025-05-07 09:32:14', 1, 0),
(3, 'user12345', 'bablumahto7061@gmail.com', 22, 'Male', 'scrypt:32768:8:1$STjXUGayatBeSIcA$065b3b8e90d784f7a2fb532cf34b8f7b13fedef44b4439de270fda88630fee66da42dbe4c7673142814fd1a133007b37f4f65ba0de860b3b1a3266edba220258', 0, '2025-05-07 09:32:14', 1, 0),
(4, 'Biswajit', 'biswajitsenapati8106@gmail.com', 21, 'Male', 'scrypt:32768:8:1$VWSOGwL73W0WhQBy$cfdd6bd406214fab644c430b075e04c5d869ec23645752a34a62628de6a663f4d1839cb586312cd23e577c237d288cc0f57b54fe6171fddd5c4aca358723af4d', 0, '2025-05-07 09:32:14', 1, 0),
(5, 'Arav', 'arav@gmail.com', 54, 'Male', 'scrypt:32768:8:1$iRruBlCSAVnu3l08$79cfd37ca4f14d2eb1b03a06be5919a5c4e817cf5e86f0118273d5162fa133f281b52071d73b2083958382bca4536ae141d02ee40236fc37fb946504b9c21bb8', 0, '2025-05-07 09:32:14', 1, 0),
(7, 'Admin User', 'admin@gmail.com', 30, 'Other', 'scrypt:32768:8:1$KBGBRTJL2AgKfgxZ$b00d59a01a6a2951082c8589fc8c0f6af7374c89afe23c89f06a630a7fbec438e07893fc2f47bbec14834e1a15c66010e776a74468e0a285d3d6bedfc3f64af5', 1, '2025-05-07 09:32:14', 1, 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
