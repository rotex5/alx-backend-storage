-- script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
  IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_weighted_score FLOAT;
    
    -- Compute the total weighted score and total weight for the user
    SELECT SUM(score*weight), SUM(weight) INTO total_weighted_score, total_weight
      FROM corrections WHERE user_id = user_id;
    
    -- Compute the average weighted score
    IF total_weight > 0 THEN
        SET avg_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;
    
    -- Update the user's average weighted score in the users table
    UPDATE users SET average_weighted_score = avg_weighted_score WHERE id = user_id;
    
END$$
DELIMITER ;

