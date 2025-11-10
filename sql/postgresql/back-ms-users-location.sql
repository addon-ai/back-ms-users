-- SQL DDL for back-ms-users-location
-- Database: POSTGRESQL
-- Generated automatically from OpenAPI specification
-- Do not edit manually

-- Table for cities
CREATE TABLE IF NOT EXISTS cities (
    city_id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    region_id UUID NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cities_name ON cities (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_cities_status ON cities (status); -- Index for status field

-- Table for countries
CREATE TABLE IF NOT EXISTS countries (
    country_id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_countries_name ON countries (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_countries_status ON countries (status); -- Index for status field

-- Table for locations
CREATE TABLE IF NOT EXISTS locations (
    location_id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    user_id UUID NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    neighborhood VARCHAR(255),
    address VARCHAR(255) NOT NULL,
    postal_code VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    location_type VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updated_at TIMESTAMPTZ -- Record last update timestamp
);

CREATE INDEX IF NOT EXISTS idx_locations_status ON locations (status); -- Index for status field

-- Enumeration table for LocationType
CREATE TABLE IF NOT EXISTS locationtypes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Unique identifier
    code VARCHAR(50) NOT NULL UNIQUE, -- Enum code value
    name VARCHAR(100) NOT NULL, -- Human readable name
    description VARCHAR(255), -- Detailed description
    active BOOLEAN NOT NULL DEFAULT TRUE, -- Whether this enum value is active
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updated_at TIMESTAMPTZ -- Record last update timestamp
);

-- Enum values
INSERT INTO locationtypes (code, name, description) VALUES ('HOME', 'Home', 'LocationType - Home') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('WORK', 'Work', 'LocationType - Work') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('BILLING', 'Billing', 'LocationType - Billing') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('SHIPPING', 'Shipping', 'LocationType - Shipping') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('OTHER', 'Other', 'LocationType - Other') ON CONFLICT (code) DO NOTHING;

-- Table for neighborhoods
CREATE TABLE IF NOT EXISTS neighborhoods (
    neighborhood_id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    city_id UUID NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_neighborhoods_name ON neighborhoods (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_neighborhoods_status ON neighborhoods (status); -- Index for status field

-- Table for regions
CREATE TABLE IF NOT EXISTS regions (
    region_id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    country_id UUID NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_regions_name ON regions (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_regions_status ON regions (status); -- Index for status field