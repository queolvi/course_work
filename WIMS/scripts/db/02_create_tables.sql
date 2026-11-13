GO
USE Warehouse;

GO
CREATE TABLE dbo.ROLES(
	role_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,name NVARCHAR(50) NOT NULL 
	,description NVARCHAR(75)
	,created_at DATETIME2(0) NOT NULL CONSTRAINT ROLES_created_at DEFAULT SYSDATETIME(),

) ON [PRIMARY];

GO
CREATE TABLE dbo.USERS(
	user_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,username NVARCHAR(50) NOT NULL UNIQUE
	,password_hash NVARCHAR(255) NOT NULL UNIQUE
	,full_name NVARCHAR(175) NOT NULL
	,role_id INT NOT NULL
	,is_active BIT CONSTRAINT USER_is_active DEFAULT 1
	,created_at DATETIME2(0) NOT NULL CONSTRAINT USER_created_at DEFAULT SYSDATETIME()
	, FOREIGN KEY (role_id) REFERENCES dbo.ROLES(role_id)
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.CATEGORIES(
	category_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY
	,name NVARCHAR(125) NOT NULL
) ON [PRIMARY]
GO

GO
CREATE TABLE dbo.PRODUCTS(
	product_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,name NVARCHAR(255) NOT NULL
	,stock_keeping_unit NVARCHAR(50) NOT NULL UNIQUE
	,category_id INT NOT NULL
	,unit NVARCHAR(20) NOT NULL
	,description NVARCHAR(500)
	,min_stock INT NOT NULL CONSTRAINT PRODUCTS_min_stock DEFAULT 0
	,CONSTRAINT CK_PRODUCTS_min_stock CHECK (min_stock >= 0)
	,FOREIGN KEY (category_id) REFERENCES dbo.CATEGORIES(category_id)
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.STORAGE_LOCATIONS(
	location_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,warehouse_name NVARCHAR(100) NOT NULL
	,zone NVARCHAR(50) NOT NULL
	,shelf NVARCHAR(50) NOT NULL
	,cell NVARCHAR(50) NOT NULL
	,description NVARCHAR(255)
	,CONSTRAINT UQ_STORAGE_LOCATIONS_full UNIQUE (warehouse_name, zone, shelf, cell)
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.BATCHES(
	batch_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,product_id INT NOT NULL
	,quantity INT NOT NULL
	,reserved_quantity INT NOT NULL CONSTRAINT BATCHES_reserved DEFAULT 0
	,manufacture_date DATE NOT NULL
	,expiration_date DATE NOT NULL
	,location_id INT NOT NULL
	,created_at DATETIME2(0) NOT NULL CONSTRAINT BATCHES_created_at DEFAULT SYSDATETIME()
	,available_quantity AS (quantity - reserved_quantity) PERSISTED
	,CONSTRAINT CK_BATCHES_quantity CHECK (quantity >= 0)
	,CONSTRAINT CK_BATCHES_reserved CHECK (reserved_quantity >= 0 AND reserved_quantity <= quantity)
	,FOREIGN KEY (product_id) REFERENCES dbo.PRODUCTS(product_id)
	,FOREIGN KEY (location_id) REFERENCES dbo.STORAGE_LOCATIONS(location_id)
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.CUSTOMERS(
	customer_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,user_id INT NULL
	,name NVARCHAR(200) NOT NULL
	,inn NVARCHAR(12) NULL
	,contact NVARCHAR(100) NOT NULL
	,city NVARCHAR(50)
	,street NVARCHAR(100)
	,building NVARCHAR(20)
	,apartment NVARCHAR(20)
	,CONSTRAINT UQ_CUSTOMERS_user UNIQUE (user_id)
	,CONSTRAINT CK_CUSTOMERS_inn CHECK (inn IS NULL OR LEN(inn) = 10 OR LEN(inn) = 12)
	,FOREIGN KEY (user_id) REFERENCES dbo.USERS(user_id) ON DELETE SET NULL
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.ORDERS(
	order_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,customer_id INT NOT NULL
	,user_id INT NOT NULL
	,status NVARCHAR(20) NOT NULL CONSTRAINT ORDERS_status DEFAULT N'new'
	,created_at DATETIME2(0) NOT NULL CONSTRAINT ORDERS_created_at DEFAULT SYSDATETIME()
	,CONSTRAINT CK_ORDERS_status CHECK (status IN (N'new', N'processing', N'completed', N'cancelled'))
	,FOREIGN KEY (customer_id) REFERENCES dbo.CUSTOMERS(customer_id)
	,FOREIGN KEY (user_id) REFERENCES dbo.USERS(user_id)
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.ORDER_ITEMS(
	order_item_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,order_id INT NOT NULL
	,batch_id INT NOT NULL
	,quantity INT NOT NULL
	,price DECIMAL(12,2) NOT NULL
	,CONSTRAINT CK_ORDER_ITEMS_quantity CHECK (quantity > 0)
	,CONSTRAINT CK_ORDER_ITEMS_price CHECK (price >= 0)
	,FOREIGN KEY (order_id) REFERENCES dbo.ORDERS(order_id) ON DELETE CASCADE
	,FOREIGN KEY (batch_id) REFERENCES dbo.BATCHES(batch_id)
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.RESERVATIONS(
	reservation_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,batch_id INT NOT NULL
	,user_id INT NOT NULL
	,order_id INT NULL
	,quantity INT NOT NULL
	,status NVARCHAR(20) NOT NULL CONSTRAINT RESERVATIONS_status DEFAULT N'active'
	,created_at DATETIME2(0) NOT NULL CONSTRAINT RESERVATIONS_created_at DEFAULT SYSDATETIME()
	,expires_at DATETIME2(0) NOT NULL
	,CONSTRAINT CK_RESERVATIONS_quantity CHECK (quantity > 0)
	,CONSTRAINT CK_RESERVATIONS_expires CHECK (expires_at > created_at)
	,CONSTRAINT CK_RESERVATIONS_status CHECK (status IN (N'active', N'fulfilled', N'cancelled'))
	,FOREIGN KEY (batch_id) REFERENCES dbo.BATCHES(batch_id)
	,FOREIGN KEY (user_id) REFERENCES dbo.USERS(user_id)
	,FOREIGN KEY (order_id) REFERENCES dbo.ORDERS(order_id) ON DELETE SET NULL
) ON [PRIMARY];
GO

GO
CREATE TABLE dbo.DOCUMENTS(
	document_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,type NVARCHAR(30) NOT NULL
	,number NVARCHAR(50) NOT NULL
	,doc_date DATE NOT NULL
	,user_id INT NOT NULL
	,status NVARCHAR(20) NOT NULL CONSTRAINT DOCUMENTS_status DEFAULT N'draft'
	,CONSTRAINT UQ_DOCUMENTS_number UNIQUE (type, number)
	,CONSTRAINT CK_DOCUMENTS_type CHECK (type IN (N'invoice', N'waybill', N'write_off_act'))
	,CONSTRAINT CK_DOCUMENTS_status CHECK (status IN (N'draft', N'approved', N'cancelled'))
	,FOREIGN KEY (user_id) REFERENCES dbo.USERS(user_id)
) ON [PRIMARY];
GO


GO
CREATE TABLE dbo.STOCK_MOVEMENTS(
	movement_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
	,batch_id INT NOT NULL
	,type NVARCHAR(20) NOT NULL
	,quantity INT NOT NULL
	,user_id INT NOT NULL
	,document_id INT NULL
	,created_at DATETIME2(0) NOT NULL CONSTRAINT STOCK_MOVEMENTS_created_at DEFAULT SYSDATETIME()
	,CONSTRAINT CK_STOCK_MOVEMENTS_type CHECK (type IN (N'receipt', N'shipment', N'write_off', N'adjustment'))
	,CONSTRAINT CK_STOCK_MOVEMENTS_quantity CHECK (quantity <> 0)
	,FOREIGN KEY (batch_id) REFERENCES dbo.BATCHES(batch_id)
	,FOREIGN KEY (user_id) REFERENCES dbo.USERS(user_id)
	,FOREIGN KEY (document_id) REFERENCES dbo.DOCUMENTS(document_id)
) ON [PRIMARY];
GO