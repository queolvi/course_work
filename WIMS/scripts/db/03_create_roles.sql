USE Warehouse;
GO


IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'db_warehouse_admin' AND type = 'R')
    CREATE ROLE db_warehouse_admin;
GO

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'db_warehouse_manager' AND type = 'R')
    CREATE ROLE db_warehouse_manager;
GO

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'db_warehouse_operator' AND type = 'R')
    CREATE ROLE db_warehouse_operator;
GO

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'db_warehouse_reader' AND type = 'R')
    CREATE ROLE db_warehouse_reader;
GO

GRANT ALTER, CONTROL, DELETE, EXECUTE, INSERT, REFERENCES, SELECT, UPDATE, VIEW DEFINITION
ON SCHEMA::dbo TO db_warehouse_admin;
GO


GRANT SELECT, INSERT, UPDATE, DELETE ON CATEGORIES TO db_warehouse_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON PRODUCTS TO db_warehouse_manager;
GRANT SELECT ON STORAGE_LOCATIONS TO db_warehouse_manager;

GRANT SELECT, INSERT, UPDATE, DELETE ON CUSTOMERS TO db_warehouse_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON ORDERS TO db_warehouse_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON ORDER_ITEMS TO db_warehouse_manager;

GRANT SELECT, INSERT, UPDATE, DELETE ON RESERVATIONS TO db_warehouse_manager;

GRANT SELECT ON BATCHES TO db_warehouse_manager;
GRANT SELECT ON STOCK_MOVEMENTS TO db_warehouse_manager;
GRANT SELECT ON DOCUMENTS TO db_warehouse_manager;

GRANT SELECT ON USERS TO db_warehouse_manager;
GRANT SELECT ON ROLES TO db_warehouse_manager;
GO

GRANT SELECT ON CATEGORIES TO db_warehouse_operator;
GRANT SELECT ON PRODUCTS TO db_warehouse_operator;
GRANT SELECT ON STORAGE_LOCATIONS TO db_warehouse_operator;

GRANT SELECT ON CUSTOMERS TO db_warehouse_operator;

GRANT SELECT, UPDATE ON ORDERS TO db_warehouse_operator;
GRANT SELECT ON ORDER_ITEMS TO db_warehouse_operator;

GRANT SELECT, UPDATE ON BATCHES TO db_warehouse_operator;

GRANT SELECT, INSERT, UPDATE ON STOCK_MOVEMENTS TO db_warehouse_operator;
GRANT SELECT, INSERT, UPDATE ON DOCUMENTS TO db_warehouse_operator;

GRANT SELECT, UPDATE ON RESERVATIONS TO db_warehouse_operator;

GRANT SELECT ON USERS TO db_warehouse_operator;
GRANT SELECT ON ROLES TO db_warehouse_operator;
GO

GRANT SELECT ON CATEGORIES TO db_warehouse_reader;
GRANT SELECT ON PRODUCTS TO db_warehouse_reader;
GRANT SELECT ON STORAGE_LOCATIONS TO db_warehouse_reader;
GRANT SELECT ON BATCHES TO db_warehouse_reader;
GRANT SELECT ON CUSTOMERS TO db_warehouse_reader;
GRANT SELECT ON ORDERS TO db_warehouse_reader;
GRANT SELECT ON ORDER_ITEMS TO db_warehouse_reader;
GRANT SELECT ON RESERVATIONS TO db_warehouse_reader;
GRANT SELECT ON STOCK_MOVEMENTS TO db_warehouse_reader;
GRANT SELECT ON DOCUMENTS TO db_warehouse_reader;
GRANT SELECT ON USERS TO db_warehouse_reader;
GRANT SELECT ON ROLES TO db_warehouse_reader;
GO

USE master;
GO


IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'app_login')
    CREATE LOGIN app_login 
    WITH PASSWORD = N'app_pswd',
         CHECK_POLICY = ON,
         DEFAULT_DATABASE = Warehouse;
GO


IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'manager_login')
    CREATE LOGIN manager_login 
    WITH PASSWORD = N'manager_pswd!',
         CHECK_POLICY = ON,
         DEFAULT_DATABASE = Warehouse;
GO


IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'audit_login')
    CREATE LOGIN audit_login 
    WITH PASSWORD = N'aidit_pswd',
         CHECK_POLICY = ON,
         DEFAULT_DATABASE = Warehouse;
GO

GO
USE Warehouse;
GO

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'app_user')
BEGIN
    IF EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'app_login')
    BEGIN
        CREATE USER app_user FOR LOGIN app_login;
        ALTER ROLE db_warehouse_operator ADD MEMBER app_user;
        PRINT N'app user created';
    END
    ELSE
        PRINT N'login for app user not found';
END
ELSE
    PRINT N'app user has already been created';
GO

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'manager_user')
BEGIN
    IF EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'manager_login')
    BEGIN
        CREATE USER manager_user FOR LOGIN manager_login;
        ALTER ROLE db_warehouse_manager ADD MEMBER manager_user;
        PRINT N'manager created';
    END
    ELSE
        PRINT N'login for manager not found';
END
ELSE
    PRINT N'manager has already been created';
GO

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'audit_user')
BEGIN
    IF EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'audit_login')
    BEGIN
        CREATE USER audit_user FOR LOGIN audit_login;
        ALTER ROLE db_warehouse_reader ADD MEMBER audit_user;
        PRINT N'audit user created';
    END
    ELSE
        PRINT N'login for audit user not found';
END
ELSE
    PRINT N'audit user has already been created';
GO

