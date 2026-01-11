
CREATE DATABASE IF NOT EXISTS SRA;
USE SRA;
CREATE TABLE IF NOT EXISTS user_data (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email_ID VARCHAR(50) NOT NULL,
    resume_score VARCHAR(8) NOT NULL,
    Timestamp VARCHAR(50) NOT NULL,
    Page_no VARCHAR(5) NOT NULL,
    Predicted_Field VARCHAR(25) NOT NULL,
    User_level VARCHAR(30) NOT NULL,
    Actual_skills VARCHAR(300) NOT NULL
);
INSERT INTO user_data 
(Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills)
VALUES
(
 'Student1',
 'student1@gmail.com',
 '85%',
 '2025-03-10_14:30:00',
 '1',
 'Data Science',
 'Fresher',
 'Python, SQL, ML'
);
SELECT * FROM user_data;
