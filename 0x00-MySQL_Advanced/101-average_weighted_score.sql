-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
-- Requirements:
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER$$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS U, 
      (SELECT U.id, SUM(score * weight) / SUM(weight) AS weight_avg 
      FROM users AS S_U 
      JOIN corrections AS C ON S_U.id=C.user_id 
      JOIN projects AS P ON C.project_id=P.id 
      GROUP BY S_U.id)
  AS AW
  SET U.average_score = AW.weight_avg
  WHERE U.id=AW.id;
END$$
DELIMITER;
