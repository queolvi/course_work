USE master;
GO

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = N'Warehouse')
BEGIN
    CREATE DATABASE Warehouse
    ON PRIMARY
    (
        NAME = N'warehouse_data',
        FILENAME = N'C:\MSSQL\Data\warehouse_data.mdf',
        SIZE = 100MB,
        MAXSIZE = UNLIMITED,
        FILEGROWTH = 50MB
    ),
    FILEGROUP FG_INDEX
    (
        NAME = N'warehouse_index',
        FILENAME = N'C:\MSSQL\Index\warehouse_index.ndf',
        SIZE = 50MB,
        MAXSIZE = UNLIMITED,
        FILEGROWTH = 25MB
    ),
    FILEGROUP FG_AUDIT
    (
        NAME = N'warehouse_audit',
        FILENAME = N'C:\MSSQL\Audit\warehouse_audit.ndf',
        SIZE = 50MB,
        MAXSIZE = UNLIMITED,
        FILEGROWTH = 25MB
    )
    LOG ON
    (
        NAME = N'warehouse_log',
        FILENAME = N'C:\MSSQL\Log\warehouse_log.ldf',
        SIZE = 200MB,
        MAXSIZE = 2GB,
        FILEGROWTH = 100MB
    );
    
    PRINT N'db created';
END
ELSE
BEGIN
    PRINT N'db has been created before, cant create again';
END
GO