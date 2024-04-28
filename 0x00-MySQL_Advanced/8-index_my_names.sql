-- script that creates an index idx_name_first on the
-- table names and the first letter of name.
ALTER TABLE names ADD COLUMN name_first_letter CHAR(1)
GENERATED ALWAYS AS (LEFT(name, 1));
CREATE INDEX idx_name_first ON names (name);
