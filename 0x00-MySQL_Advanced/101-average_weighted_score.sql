-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
-- Requirements:
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    UPDATE users set average_score = (
    SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
    FROM corrections as C
    INNER JOIN projects AS P ON P.id = C.project_id
    where C.user_id = users.id);
END $$
DELIMITER ;
