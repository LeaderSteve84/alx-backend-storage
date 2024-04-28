-- script that creates an index idx_name_first_score
-- on the table names and the first letter of name and the score.
ALTER TABLE names ADD COLUMN name_first_char CHAR(1)
GENERATED ALWAYS AS (LEFT(name, 1));
CREATE INDEX idx_name_first_score ON names ( name, score);
