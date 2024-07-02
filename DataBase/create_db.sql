-- Drop tables if they exist
DROP TABLE IF EXISTS "reservation_status";
DROP TABLE IF EXISTS "reservations";
DROP TABLE IF EXISTS "equipment_reservations";
DROP TABLE IF EXISTS "equipment_inventory";
DROP TABLE IF EXISTS "equipment_category";
DROP TABLE IF EXISTS "equipment_details";
DROP TABLE IF EXISTS "addresses";
DROP TABLE IF EXISTS "user_signup_status";
DROP TABLE IF EXISTS "accounts";
DROP TABLE IF EXISTS "roles";

-- Table to store account information
CREATE TABLE "accounts" (
	"ACCOUNT_ID"	INTEGER NOT NULL UNIQUE, -- Unique account identifier
	"FIRST_NAME"	TEXT NOT NULL, -- First name of the account holder
	"LAST_NAME"	TEXT NOT NULL, -- Last name of the account holder
	"USER_NAME" TEXT NOT NULL UNIQUE, -- Unique username for login
	"BIRTHDATE"	TEXT NOT NULL, -- Date of birth of the account holder
	"PHONE_NUMBER"	TEXT NOT NULL, -- Phone number of the account holder
	"EMAIL"	TEXT NOT NULL UNIQUE, -- Email address of the account holder
	"PASSWORD" TEXT NOT NULL, -- Password for account login
	"ADDRESS_ID"	INTEGER NOT NULL, -- Foreign key referencing the address of the account holder
	"ROLE_ID" INTEGER NOT NULL, -- Foreign key referencing the role of the account holder
	PRIMARY KEY("ACCOUNT_ID" AUTOINCREMENT), -- Primary key for the table
	FOREIGN KEY("ADDRESS_ID") REFERENCES "addresses"("ID"), -- Foreign key constraint for address reference
	FOREIGN KEY("ROLE_ID") REFERENCES "roles"("ROLE_ID") -- Foreign key constraint for role reference
);

-- Table to define user roles
CREATE TABLE "roles" (
	"ROLE_ID"	INTEGER NOT NULL UNIQUE, -- Unique role identifier
	"ROLE_TYPE" TEXT NOT NULL CHECK("ROLE_TYPE" IN ('admin', 'user')), -- Type of role, either admin or user
	PRIMARY KEY("ROLE_ID") -- Primary key for the table
);

-- Table to track signup status of users
CREATE TABLE "user_signup_status" (
	"USER_ID"	INTEGER NOT NULL, -- Unique user identifier
	"STATUS" TEXT NOT NULL CHECK("STATUS" IN ('pending', 'approved', 'rejected')), -- Status of user signup
	PRIMARY KEY("USER_ID"), -- Primary key for the table
	FOREIGN KEY("USER_ID") REFERENCES "accounts"("ACCOUNT_ID") -- Foreign key constraint for user reference
);
-- Table to store addresses
CREATE TABLE "addresses" (
	"ID"	INTEGER, -- Unique address identifier
	"STREET"	TEXT NOT NULL, -- Street address
	"CITY"	TEXT NOT NULL, -- City
	"PROVINCE"	TEXT NOT NULL, -- Province
	"POSTAL_CODE"	TEXT NOT NULL, -- Postal code
	UNIQUE("STREET","CITY","PROVINCE","POSTAL_CODE"), -- Ensure address uniqueness
	PRIMARY KEY("ID" AUTOINCREMENT) -- Primary key for the table
);

-- Table to store equipment details
CREATE TABLE "equipment_details" (
	"ID"	INTEGER NOT NULL UNIQUE, -- Unique equipment identifier
	"CATEGORY_ID" INTEGER NOT NULL, -- Foreign key referencing equipment category
	"AVAILABILITY_ID" INTEGER NOT NULL, -- Foreign key referencing equipment availability
	"NAME"	TEXT NOT NULL, -- Name of the equipment
	"DESCRIPTION" TEXT NOT NULL, -- Description of the equipment
	"IS_ONSITE_ONLY" INTEGER NOT NULL CHECK("IS_ONSITE_ONLY" IN (0, 1)), -- Flag indicating if equipment is onsite only
	"WARRANTY_YEARS" INTEGER NOT NULL, -- Warranty duration in years
	PRIMARY KEY("ID" AUTOINCREMENT), -- Primary key for the table
	FOREIGN KEY("CATEGORY_ID") REFERENCES "equipment_category"("CATEGORY_ID") -- Foreign key constraint for category reference
	FOREIGN KEY("AVAILABILITY_ID") REFERENCES "equipment_inventory"("ID")
);

-- Table to store equipment categories
CREATE TABLE "equipment_category" (
	"CATEGORY_ID"	INTEGER NOT NULL UNIQUE, -- Unique category identifier
	"CATEGORY_NAME"	TEXT NOT NULL, -- Name of the category
	PRIMARY KEY("CATEGORY_ID" AUTOINCREMENT) -- Primary key for the table
);

-- Table to manage equipment inventory
CREATE TABLE "equipment_inventory" (
	"ID"	INTEGER NOT NULL UNIQUE, -- Unique inventory identifier
	"LENT" INTEGER NOT NULL, -- Number of equipment lent
	"AVAILABLE" INTEGER NOT NULL, -- Number of equipment available
	PRIMARY KEY("ID"), -- Primary key for the table
	FOREIGN KEY("ID") REFERENCES "equipment_details"("ID") -- Foreign key constraint for equipment details reference
);

-- Table to manage equipment reservations
CREATE TABLE "equipment_reservations" (
	"ID"	INTEGER NOT NULL UNIQUE, -- Unique reservation identifier
	"EQUIPMENT_ID" INTEGER NOT NULL, -- Foreign key referencing equipment details
	"RESERVATION_ID" INTEGER, -- Foreign key referencing reservations
	"BORROW_DATE" TEXT NOT NULL, -- Date of borrowing equipment
	"RETURN_DATE" TEXT NOT NULL, -- Date of returning equipment
	"PURPOSE"	TEXT NOT NULL, -- Purpose of reservation
	"RESERVATION_TYPE" TEXT NOT NULL CHECK(RESERVATION_TYPE IN ('onsite', 'borrow')), -- Type of reservation
	PRIMARY KEY("ID" AUTOINCREMENT), -- Primary key for the table
	FOREIGN KEY("RESERVATION_ID") REFERENCES "reservations"("RESERVATION_ID"), -- Foreign key constraint for reservation reference
	FOREIGN KEY("EQUIPMENT_ID") REFERENCES "equipment_details"("ID") -- Foreign key constraint for equipment reference
);

-- Table to store reservations
CREATE TABLE "reservations" (
	"RESERVATION_ID"	INTEGER NOT NULL, -- Unique reservation identifier
	"USER_ID" INTEGER NOT NULL, -- Foreign key referencing users
	"CREATED_DATE" TEXT NOT NULL, -- Date of reservation creation
	"CREATED_TIME"	TEXT NOT NULL, -- Time of reservation creation
	PRIMARY KEY("RESERVATION_ID" AUTOINCREMENT), -- Primary key for the table
	FOREIGN KEY("USER_ID") REFERENCES "accounts"("ACCOUNT_ID") -- Foreign key constraint for user reference
);

-- Table to store reservation status
CREATE TABLE "reservation_status" (
	"RESERVATION_ID"	INTEGER NOT NULL, -- Unique reservation identifier
	"STATUS" TEXT NOT NULL CHECK(STATUS IN ('pending', 'approved', 'rejected')), -- Status of reservation
	PRIMARY KEY("RESERVATION_ID"), -- Primary key for the table
	FOREIGN KEY("RESERVATION_ID") REFERENCES "reservations"("RESERVATION_ID") -- Foreign key constraint for reservation reference
);

INSERT INTO "roles" ("ROLE_TYPE") VALUES ('admin'), ('user');
INSERT INTO "addresses" ("STREET", "CITY", "PROVINCE", "POSTAL_CODE")
VALUES ('123 Main St', 'Anytown', 'Anystate', '12345');
INSERT INTO "accounts" ("FIRST_NAME", "LAST_NAME", "USER_NAME", "BIRTHDATE", "PHONE_NUMBER", "EMAIL", "PASSWORD", "ADDRESS_ID", "ROLE_ID")
VALUES ('John', 'Doe', 'johndoe', '1990-01-01', '1234567890', 'johndoe@example.com', 'password123', 1, (SELECT "ROLE_ID" FROM "roles" WHERE "ROLE_TYPE" = 'admin'));
