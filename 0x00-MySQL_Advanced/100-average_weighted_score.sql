-- script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
  user_id INTEGER)
BEGIN
    DECLARE avg_weighted_score FLOAT;
    SET avg_weighted_score = (
      SELECT SUM(score * weight) / SUM(weight)
        FROM users AS U 
        JOIN corrections as C ON U.id=C.user_id 
        JOIN projects AS P ON C.project_id=P.id 
        WHERE U.id=user_id);
 
    -- Update the user's average weighted score in the users table
    UPDATE users SET average_score = avg_weighted_score WHERE id=user_id;
    
END$$
DELIMITER ;

