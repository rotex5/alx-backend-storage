-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
-- Requirements:
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER$$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS U, 
      (SELECT users.id, SUM(score * weight) / SUM(weight) AS weight_avg 
      FROM users as S_U 
      JOIN corrections ON S_U.id=corrections.user_id 
      JOIN projects ON corrections.project_id=projects.id 
      GROUP BY S_U.id)
  AS AW
  SET U.average_score = AW.weight_avg
  WHERE U.id=AW.id;
END$$
DELIMITER;
