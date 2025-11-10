-- SQL DDL for back-ms-users
-- Database: POSTGRESQL
-- Generated automatically from OpenAPI specification
-- Do not edit manually

-- Table for users
CREATE TABLE IF NOT EXISTS users (
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier -- Unique identifier for the user account. Generated automatically upon creation
    username VARCHAR(255) NOT NULL UNIQUE, -- Users unique username. Cannot be changed after account creation
    email VARCHAR(255) NOT NULL UNIQUE, -- Users email address. Used for notifications and account recovery
    first_name VARCHAR(255), -- Users first name. May be null if not provided during registration
    last_name VARCHAR(255), -- Users last name. May be null if not provided during registration
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL, -- Timestamp when the user account was created. ISO 8601 format
    updated_at TIMESTAMPTZ NOT NULL -- Timestamp when the user account was last updated. ISO 8601 format
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users (username); -- Users unique username. Cannot be changed after account creation

CREATE INDEX IF NOT EXISTS idx_users_email ON users (email); -- Users email address. Used for notifications and account recovery

CREATE INDEX IF NOT EXISTS idx_users_first_name ON users (first_name); -- Users first name. May be null if not provided during registration

CREATE INDEX IF NOT EXISTS idx_users_last_name ON users (last_name); -- Users last name. May be null if not provided during registration

CREATE INDEX IF NOT EXISTS idx_users_status ON users (status); -- Index for status field

-- Enumeration table for UserStatus
CREATE TABLE IF NOT EXISTS userstatuss (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Unique identifier
    code VARCHAR(50) NOT NULL UNIQUE, -- Enum code value
    name VARCHAR(100) NOT NULL, -- Human readable name
    description VARCHAR(255), -- Detailed description
    active BOOLEAN NOT NULL DEFAULT TRUE, -- Whether this enum value is active
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updated_at TIMESTAMPTZ -- Record last update timestamp
);

-- Enum values
INSERT INTO userstatuss (code, name, description) VALUES ('ACTIVE', 'Active', 'UserStatus - Active') ON CONFLICT (code) DO NOTHING;
INSERT INTO userstatuss (code, name, description) VALUES ('INACTIVE', 'Inactive', 'UserStatus - Inactive') ON CONFLICT (code) DO NOTHING;
INSERT INTO userstatuss (code, name, description) VALUES ('SUSPENDED', 'Suspended', 'UserStatus - Suspended') ON CONFLICT (code) DO NOTHING;