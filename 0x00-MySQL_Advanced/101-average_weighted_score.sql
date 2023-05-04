-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
-- Requirements:
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER$$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users, 
      (SELECT users.id, SUM(score * weight) / SUM(weight) AS weight_avg 
      FROM users 
      JOIN corrections ON users.id=corrections.user_id 
      JOIN projects ON corrections.project_id=projects.id 
      GROUP BY users.id)
  AS AW
  SET users.average_score = AW.weight_avg
  WHERE users.id=AW.id;
END$$
DELIMITER;
