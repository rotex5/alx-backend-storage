-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.
-- Note: An average score can be a decimal
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INTEGER)
BEGIN
    DECLARE avg_score DECIMAL(10,2);
    SET avg_score = (SELECT AVG(score) FROM corrections  WHERE corrections.user_id=user_id);

    -- Update the user's average score in the users table
    UPDATE users SET average_score = avg_score WHERE id=user_id;
END$$
DELIMITER;
