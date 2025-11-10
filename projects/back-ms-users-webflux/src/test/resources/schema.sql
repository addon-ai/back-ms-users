-- Test Schema for H2 Database
-- Automatically loaded by Spring Boot for tests

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    user_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: countries
CREATE TABLE IF NOT EXISTS countries (
    country_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: regions
CREATE TABLE IF NOT EXISTS regions (
    region_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    country_id VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: cities
CREATE TABLE IF NOT EXISTS cities (
    city_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region_id VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: neighborhoods
CREATE TABLE IF NOT EXISTS neighborhoods (
    neighborhood_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: locations
CREATE TABLE IF NOT EXISTS locations (
    location_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
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
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
