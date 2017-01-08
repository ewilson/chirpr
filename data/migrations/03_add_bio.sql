ALTER TABLE user ADD COLUMN bio TEXT;
UPDATE user SET bio = '';
