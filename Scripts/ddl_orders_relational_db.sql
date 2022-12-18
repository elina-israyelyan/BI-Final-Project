USE master;

CREATE DATABASE Orders_RELATIONAL_DB;

USE Orders_RELATIONAL_DB;

CREATE TABLE Region(RegionID INTEGER PRIMARY KEY NOT NULL,
				RegionDescription NCHAR(50) NOT NULL);


CREATE TABLE Territories(
	TerritoryID NVARCHAR(20) PRIMARY KEY NOT NULL,
	TerritoryDescription  NCHAR(50) NOT NULL,
	RegionID INTEGER NOT NULL,
	CONSTRAINT territory_region FOREIGN KEY(RegionID)  REFERENCES Region(RegionID)
);
				
CREATE TABLE Categories(
	CategoryID INTEGER PRIMARY KEY NOT NULL,
	CategoryName NVARCHAR(15) NOT NULL,
	Description VARCHAR(MAX),
	Picture IMAGE
);

CREATE TABLE Suppliers(
	SupplierID INTEGER NOT NULL PRIMARY KEY,
	CompanyName NVARCHAR(40) NOT NULL,
	ContactName NVARCHAR(30),
	ContactTitle NVARCHAR(30),
	Address NVARCHAR(60),
	City NVARCHAR(15),
	Region NVARCHAR(15),
	PostalCode NVARCHAR(10),
	Country NVARCHAR(15),
	Phone NVARCHAR(24),
	Fax NVARCHAR(24),
	HomePage VARCHAR(MAX)
);
CREATE TABLE Customers(
	CustomerID NCHAR(5) NOT NULL PRIMARY KEY,
	CompanyName NVARCHAR(40) NOT NULL,
	ContactName NVARCHAR(30),
	ContactTitle NVARCHAR(30),
	Address NVARCHAR(60),
	City NVARCHAR(15),
	Region NVARCHAR(15),
	PostalCode NVARCHAR(10),
	Country NVARCHAR(15),
	Phone NVARCHAR(24),
	Fax NVARCHAR(24)
);

CREATE TABLE Shippers(
	ShipperID INTEGER NOT NULL PRIMARY KEY,
	CompanyName NVARCHAR(40) NOT NULL,
	Phone NVARCHAR(24)
);

CREATE TABLE Products(
	ProductID INTEGER NOT NULL PRIMARY KEY,
	ProductName NVARCHAR(40) NOT NULL,
	SupplierID INTEGER,
	CategoryID INTEGER,
	QuantityPerUnit NVARCHAR(20),
	UnitPrice MONEY,
	UnitsInStock SMALLINT,
	UnitsOnOrder SMALLINT,
	ReorderLevel SMALLINT,
	Discontinued BIT NOT NULL,
	CONSTRAINT supplier_product FOREIGN KEY(SupplierID)  REFERENCES Suppliers(SupplierID),
	CONSTRAINT category_product FOREIGN KEY(CategoryID)  REFERENCES Categories(CategoryID)

	
);

CREATE TABLE Employees(
	EmployeeID INTEGER NOT NULL PRIMARY KEY,
	LastName NVARCHAR(20) NOT NULL,
	FirstName NVARCHAR(10) NOT NULL,
	Title NVARCHAR(30),
	TitleOfCourtesy NVARCHAR(25),
	BirthDate DATETIME,
	HireDate DATETIME,
	Address NVARCHAR(60),
	City NVARCHAR(15),
	Region NVARCHAR(15),
	PostalCode NVARCHAR(10),
	Country NVARCHAR(15),
	HomePhone NVARCHAR(24),
	Extension NVARCHAR(4),
	PHOTO IMAGE,
	Notes VARCHAR(MAX),
	ReportsTo INTEGER,
	PhotoPath NVARCHAR(255),
	CONSTRAINT employee_reports_to FOREIGN KEY(ReportsTo)  REFERENCES Employees(EmployeeID),

);

CREATE TABLE EmployeeTerritories(
	EmployeeID INTEGER NOT NULL,
	TerritoryID NVARCHAR(20) NOT NULL,
    CONSTRAINT employee_territory_pk PRIMARY KEY (EmployeeID, TerritoryID),
	CONSTRAINT employee_territory FOREIGN KEY(EmployeeID)  REFERENCES Employees(EmployeeID),
	CONSTRAINT territory_employee FOREIGN KEY(TerritoryID)  REFERENCES Territories(TerritoryID)

);

CREATE TABLE Orders(
	OrderID INTEGER NOT NULL PRIMARY KEY,
	CustomerID NCHAR(5),
	EmployeeID INTEGER,
	OrderDate DATETIME,
	RequiredDate DATETIME,
	ShippedDate DATETIME,
	ShipVia INTEGER,
	Freight MONEY,
	ShipName NVARCHAR(40),
	ShipAddress NVARCHAR(60),
	ShipCity NVARCHAR(15),
	ShipRegion NVARCHAR(15),
	ShipPostalCode NVARCHAR(10),
	ShipCountry NVARCHAR(15),
	CONSTRAINT order_employee FOREIGN KEY(EmployeeID)  REFERENCES Employees(EmployeeID),
	CONSTRAINT order_shippers FOREIGN KEY(ShipVia)  REFERENCES Shippers(ShipperID),
	CONSTRAINT order_customers FOREIGN KEY(CustomerID)  REFERENCES Customers(CustomerID),

	
);


CREATE TABLE OrderDetails(
	OrderID INTEGER NOT NULL,
	ProductID INTEGER 	NOT NULL,
	UnitPrice MONEY NOT NULL,
	Quantity  SMALLINT NOT NULL,
	Discount REAL NOT NULL,
   	CONSTRAINT orders_products_pk PRIMARY KEY (OrderID, ProductID),
	CONSTRAINT orders_product FOREIGN KEY(OrderID)  REFERENCES Orders(OrderID),
	CONSTRAINT products_order FOREIGN KEY(ProductID)  REFERENCES Products(ProductID)

);

