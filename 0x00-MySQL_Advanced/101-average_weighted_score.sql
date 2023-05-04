-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
-- Requirements:
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS U
    JOIN (
        SELECT user_id, SUM(score * weight) / SUM(weight) AS avg_weighted_score
        FROM corrections
        GROUP BY user_id
    ) AS C ON U.id = C.user_id
    SET U.average_weighted_score = C.avg_weighted_score;
END$$
DELIMITER ;
