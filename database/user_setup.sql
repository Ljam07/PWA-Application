-- Step 1: Create the table
CREATE TABLE IF NOT EXISTS Users (
    email TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    password TEXT NOT NULL,
    permission INTEGER NOT NULL
);

-- Step 2: Insert the data into the table
-- INSERT INTO Users (email, username, firstname, lastname, password, permission)
-- VALUES
--     ('admin@xyz', 'admin', 'admin', 'istrator', 'adminpw', 1),
--     ('john.doe@example.com', 'johndoe', 'John', 'Doe', 'securepassword123', 2);
-- 