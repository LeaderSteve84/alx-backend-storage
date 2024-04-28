-- script that creates an index idx_name_first on the
-- table names and the first letter of name.
ALTER TABLE names ADD COLUMN name CHAR(1);
UPDATE names SET name = LEFT(name, 1);
CREATE INDEX idx_name_first ON names (name);
