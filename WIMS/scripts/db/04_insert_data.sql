GO
USE Warehouse;

GO
INSERT INTO dbo.ROLES (name, description) VALUES
('ADMIN', 'System administrator')
,('MANAGER', 'Manager')
,('WAREHOUSE', 'Warehouse operator')
,('CUSTOMER', 'Customer')
,('READER', 'Reader');
GO

GO
INSERT INTO dbo.USERS (username, password_hash, full_name, role_id, is_active) VALUES
('admin', 'hash_admin_123', 'Ivanov Ivan Ivanovich', 1, 1)
,('manager', 'hash_manager_123', 'Petrova Maria Sergeevna', 2, 1)
,('operator', 'hash_operator_123', 'Sidorov Petr Alekseevich', 3, 1)
,('customer1', 'hash_customer1_123', 'OOO Romashka', 4, 1)
,('auditor', 'hash_auditor_123', 'Smirnov Aleksey Petrovich', 5, 1);
GO

GO
INSERT INTO dbo.CATEGORIES (name) VALUES
('Food products')
,('Pharmaceuticals')
,('Household chemicals')
,('Dairy products')
,('Meat products')
,('Bakery products')
,('Antibiotics')
,('Vitamins')
,('Yogurts')
,('Milk')
,('Sour cream');
GO

GO
INSERT INTO dbo.PRODUCTS (name, stock_keeping_unit, category_id, unit, description, min_stock) VALUES
('Strawberry yogurt 150g', 'YOG-STR-150', 9, 'pcs', 'Strawberry yogurt', 50)
,('Milk 3.2% 1L', 'MLK-32-1L', 10, 'pcs', 'Pasteurized milk 3.2%', 30)
,('Sour cream 20% 300g', 'SMT-20-300', 11, 'pcs', 'Sour cream 20%', 20)
,('Chicken fillet 1kg', 'CHK-FIL-1K', 5, 'kg', 'Chilled chicken fillet', 15)
,('White sliced bread 400g', 'BRD-WHT-400', 6, 'pcs', 'Wheat sliced bread', 25)
,('Amoxicillin 500mg 20pcs', 'AMX-500-20', 7, 'pack', 'Broad-spectrum antibiotic', 10)
,('Vitamin D3 2000IU 30pcs', 'VTD3-2000-30', 8, 'pack', 'Vitamin D3 capsules', 15)
,('Dish soap 1L', 'DWS-1L-001', 3, 'pcs', 'Dish soap', 40)
,('Kefir 1% 500ml', 'KFR-1-500', 10, 'pcs', 'Kefir 1%', 25)
,('Boiled sausage Doctor 400g', 'CLB-DOC-400', 5, 'pcs', 'Boiled sausage', 20);
GO

GO
INSERT INTO dbo.STORAGE_LOCATIONS (warehouse_name, zone, shelf, cell, description) VALUES
('Warehouse 1', 'A', '1', '01', 'Cold storage +4C')
,('Warehouse 1', 'A', '1', '02', 'Cold storage +4C')
,('Warehouse 1', 'A', '2', '01', 'Cold storage +4C')
,('Warehouse 1', 'B', '1', '01', 'Freezer -18C')
,('Warehouse 1', 'C', '1', '01', 'Dry storage +20C')
,('Warehouse 1', 'C', '1', '02', 'Dry storage +20C')
,('Warehouse 1', 'D', '1', '01', 'Pharma zone +15..+20C')
,('Warehouse 1', 'D', '1', '02', 'Pharma zone +15..+20C');
GO

GO
INSERT INTO dbo.BATCHES (product_id, quantity, reserved_quantity, manufacture_date, expiration_date, location_id) VALUES
(1, 100, 30, '2026-10-01', '2026-11-20', 1)
,(1, 150, 20, '2026-10-15', '2026-12-15', 1)
,(1, 200, 0, '2026-11-01', '2027-01-10', 2)
,(1, 80, 0, '2026-11-10', '2027-02-01', 2)
,(2, 50, 0, '2026-11-01', '2026-11-15', 1)
,(2, 75, 10, '2026-11-05', '2026-11-25', 1)
,(2, 100, 0, '2026-11-08', '2026-12-05', 2)
,(3, 60, 25, '2026-10-20', '2026-11-20', 1)
,(3, 90, 0, '2026-11-01', '2026-12-01', 2)
,(4, 40, 0, '2026-11-10', '2026-11-17', 1)
,(4, 60, 15, '2026-11-12', '2026-11-22', 1)
,(5, 80, 0, '2026-11-12', '2026-11-15', 5)
,(5, 120, 0, '2026-11-13', '2026-11-17', 5)
,(6, 30, 0, '2026-05-01', '2028-05-01', 7)
,(6, 50, 5, '2026-08-15', '2028-08-15', 7)
,(7, 40, 0, '2026-06-01', '2028-06-01', 8)
,(8, 150, 0, '2026-01-10', '2029-01-10', 6)
,(9, 70, 0, '2026-11-05', '2026-11-19', 1)
,(9, 85, 0, '2026-11-08', '2026-11-22', 2)
,(10, 45, 0, '2026-11-10', '2026-11-20', 1)
,(10, 55, 10, '2026-11-11', '2026-11-25', 1)
,(1, 30, 0, '2026-08-01', '2026-09-30', 1)
,(2, 20, 0, '2026-09-01', '2026-10-15', 1)
,(5, 40, 0, '2026-10-01', '2026-10-31', 5);
GO

GO
INSERT INTO dbo.CUSTOMERS (user_id, name, inn, contact, city, street, building, apartment) VALUES
(4, 'OOO Romashka', '7701234567', '+7 (495) 123-45-67', 'Moscow', 'Lenina', '10', '5')
,(NULL, 'IP Sidorov A.V.', '771234567890', '+7 (916) 555-33-22', 'Moscow', 'Mira', '25', '12')
,(NULL, 'OOO Product-Service', '7601234567', '+7 (4852) 22-33-44', 'Yaroslavl', 'Svobody', '45', NULL)
,(NULL, 'Anna Petrovna Ivanova', NULL, '+7 (903) 111-22-33', 'Yaroslavl', 'Kirova', '8', '42')
,(NULL, 'OOO Pharma-Plus', '7709876543', '+7 (495) 987-65-43', 'Moscow', 'Tverskaya', '15', '3');
GO

GO
INSERT INTO dbo.ORDERS (customer_id, user_id, status) VALUES
(1, 2, 'completed')
,(2, 2, 'processing')
,(3, 2, 'new')
,(4, 2, 'processing')
,(5, 2, 'cancelled')
,(1, 2, 'new');
GO

GO
INSERT INTO dbo.ORDER_ITEMS (order_id, batch_id, quantity, price) VALUES
(1, 1, 20, 45.00)
,(1, 5, 10, 85.00)
,(2, 10, 5, 320.00)
,(3, 12, 15, 38.00)
,(3, 8, 10, 75.00)
,(4, 14, 2, 185.00)
,(4, 16, 3, 420.00)
,(6, 18, 8, 65.00)
,(6, 20, 4, 210.00);
GO

GO
INSERT INTO dbo.RESERVATIONS (batch_id, user_id, order_id, quantity, status, created_at, expires_at) VALUES
(2, 2, 2, 20, 'active', DATEADD(HOUR, -6, GETDATE()), DATEADD(HOUR, 18, GETDATE()))
,(6, 2, 4, 10, 'active', DATEADD(HOUR, -4, GETDATE()), DATEADD(HOUR, 20, GETDATE()))
,(11, 2, NULL, 15, 'active', DATEADD(HOUR, -2, GETDATE()), DATEADD(HOUR, 24, GETDATE()))
,(15, 2, 4, 5, 'active', DATEADD(HOUR, -1, GETDATE()), DATEADD(HOUR, 48, GETDATE()))
,(21, 2, 6, 10, 'active', DATEADD(HOUR, -12, GETDATE()), DATEADD(HOUR, 12, GETDATE()))
,(1, 2, NULL, 30, 'active', DATEADD(HOUR, -30, GETDATE()), DATEADD(HOUR, -5, GETDATE()))
,(8, 2, NULL, 25, 'active', DATEADD(HOUR, -48, GETDATE()), DATEADD(HOUR, -24, GETDATE()))
,(1, 2, 1, 20, 'fulfilled', DATEADD(HOUR, -72, GETDATE()), DATEADD(HOUR, -48, GETDATE()))
,(5, 2, 1, 10, 'fulfilled', DATEADD(HOUR, -72, GETDATE()), DATEADD(HOUR, -48, GETDATE()))
,(3, 2, NULL, 50, 'cancelled', DATEADD(HOUR, -96, GETDATE()), DATEADD(HOUR, -72, GETDATE()));
GO

GO
INSERT INTO dbo.DOCUMENTS (type, number, doc_date, user_id, status) VALUES
('invoice', 'INV-0001/2026', '2026-11-10', 2, 'approved')
,('waybill', 'WB-0001/2026', '2026-11-10', 2, 'approved')
,('invoice', 'INV-0002/2026', '2026-11-11', 2, 'approved')
,('waybill', 'WB-0002/2026', '2026-11-11', 2, 'approved')
,('invoice', 'INV-0003/2026', '2026-11-12', 2, 'draft')
,('write_off_act', 'WO-0001/2026', '2026-11-13', 1, 'approved')
,('invoice', 'INV-0004/2026', '2026-11-13', 2, 'draft');
GO

GO
INSERT INTO dbo.STOCK_MOVEMENTS (batch_id, type, quantity, user_id, document_id) VALUES
(1, 'receipt', 100, 3, NULL)
,(2, 'receipt', 150, 3, NULL)
,(3, 'receipt', 200, 3, NULL)
,(4, 'receipt', 80, 3, NULL)
,(5, 'receipt', 50, 3, NULL)
,(6, 'receipt', 75, 3, NULL)
,(7, 'receipt', 100, 3, NULL)
,(14, 'receipt', 30, 3, NULL)
,(15, 'receipt', 50, 3, NULL)
,(1, 'shipment', 20, 3, 2)
,(5, 'shipment', 10, 3, 2)
,(22, 'write_off', 30, 1, 6)
,(23, 'write_off', 20, 1, 6)
,(3, 'adjustment', -5, 1, NULL);
GO

GO
SELECT 'ROLES' AS table_name, COUNT(*) AS rows_count FROM dbo.ROLES
UNION ALL SELECT 'USERS', COUNT(*) FROM dbo.USERS
UNION ALL SELECT 'CATEGORIES', COUNT(*) FROM dbo.CATEGORIES
UNION ALL SELECT 'PRODUCTS', COUNT(*) FROM dbo.PRODUCTS
UNION ALL SELECT 'STORAGE_LOCATIONS', COUNT(*) FROM dbo.STORAGE_LOCATIONS
UNION ALL SELECT 'BATCHES', COUNT(*) FROM dbo.BATCHES
UNION ALL SELECT 'CUSTOMERS', COUNT(*) FROM dbo.CUSTOMERS
UNION ALL SELECT 'ORDERS', COUNT(*) FROM dbo.ORDERS
UNION ALL SELECT 'ORDER_ITEMS', COUNT(*) FROM dbo.ORDER_ITEMS
UNION ALL SELECT 'RESERVATIONS', COUNT(*) FROM dbo.RESERVATIONS
UNION ALL SELECT 'DOCUMENTS', COUNT(*) FROM dbo.DOCUMENTS
UNION ALL SELECT 'STOCK_MOVEMENTS', COUNT(*) FROM dbo.STOCK_MOVEMENTS;
GO