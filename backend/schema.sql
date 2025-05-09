CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT,
    gender VARCHAR(10),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS diagnoses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description VARCHAR(255),
    symptoms VARCHAR(255),
    treatment VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS health_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100),
    gender VARCHAR(20),
    age INT,
    predicted_disease VARCHAR(100),
    confidence FLOAT,
    description TEXT,
    symptoms TEXT,
    precautions TEXT,
    medications TEXT,
    diets TEXT,
    workouts TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
