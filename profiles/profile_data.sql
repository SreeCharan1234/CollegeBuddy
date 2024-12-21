use profiles;
CREATE TABLE user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    leetcode_username VARCHAR(255),
    codechef_username VARCHAR(255),
    github_username VARCHAR(255),
    codeforces_username VARCHAR(255)
);
-- Insert new rows into the user_profiles table
INSERT INTO user_profiles (name, leetcode_username, codechef_username, github_username, codeforces_username)
VALUES 
('Sree Charan', 'sreecharna9484', 'sreecharna9484', 'SreeCharan1234', 'sreecharna9484'),
('ykgupta2411', 'ykgupta2411', 'ykgupta2411', 'ykgupta2411', 'ykgupta2411');

-- Query the data to verify
SELECT * FROM user_profiles;
