-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that computes and
-- store the average weighted score for all students.
DELIMITER //
CREATE PROCEDURE ComputerAverageWeightedScoreForUsers()
BEGIN
	DECLARE done INT DEFAULT FALSE;
	DECLARE cur CURSOR FOR SELECT id FROM users;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	DECLARE @user_id INT;

	OPEN cur;

	read_loop: LOOP
		FETCH cur INTO @user_id;

		IF done THEN
			LEAVE read_loop;
		END IF;

		CALL ComputeAverageWeightedScoreForUser(@user_id);
	END LOOP:

	CLOSE cur;
END //
DELIMITER ;


