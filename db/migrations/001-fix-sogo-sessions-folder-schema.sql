-- SOGo 5.12 expects sessions-specific columns: c_id, c_value (TEXT), c_creationdate, c_lastseen
-- The default OCSFolder template creates generic columns (c_folder_id, c_name, c_content, etc.)
-- which causes INSERT failures when SOGo tries to write session rows.
-- This manifests as: password accepted but cookie discarded on next request (different worker).
--
-- Fix: Drop the default template table and create with the correct schema.
--
-- NOTE: c_value is TEXT not BYTEA because SOGo's PostgreSQL client does not handle
-- the OID 17 (BYTEA) column type — it expects TEXT for session values.

DROP TABLE IF EXISTS sogo_sessions_folder;

CREATE TABLE sogo_sessions_folder (
    c_id VARCHAR(255) NOT NULL PRIMARY KEY,
    c_value TEXT NOT NULL,
    c_creationdate INTEGER NOT NULL,
    c_lastseen INTEGER NOT NULL
);
