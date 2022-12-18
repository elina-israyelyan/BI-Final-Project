import os

import pyodbc

import readconfig

path = r"/home/elina/Desktop/ayodas/bi_group_project/"
os.chdir(path)


def populate_dim_shippers_etl(cursor_ER):
    """
    Populate The Dim Shippers table from the Relational_Database
    """
    # Call to read the configuration file

    cursor_ER.execute(f'DROP PROCEDURE IF EXISTS DimShippers_ETL;')
    cursor_ER.execute(
        """
        CREATE PROCEDURE DimShippers_ETL
        AS
        BEGIN TRY
        MERGE Orders_DIMENSIONAL_DW.dbo.DimShippers AS DST -- destination
        USING Orders_RELATIONAL_DB.dbo.Shippers AS SRC -- source
        ON ( SRC.ShipperID = DST.ShipperID )
        WHEN NOT MATCHED THEN -- there are IDs in the source table that are not in the destination table
          INSERT (ShipperID,
                  CompanyName,
                  Phone)
          VALUES (SRC.ShipperID,
                  SRC.CompanyName,
                  SRC.Phone)
        WHEN MATCHED AND (  -- Isnull - a function that return a specified expression  when encountering null values 
          --Isnull(DST.clientname, '') if DST.clientname == NULL then it will return ''
          Isnull(DST.ShipperID, '') <> Isnull(SRC.ShipperID, '') OR
          Isnull(DST.CompanyName, '') <> Isnull(SRC.CompanyName, '') OR 
          Isnull(DST.Phone, '') <> Isnull(SRC.Phone, '') ) 
          THEN
            UPDATE SET DST.ShipperID = SRC.ShipperID,
                     DST.CompanyName = SRC.CompanyName,
                     DST.Phone = SRC.Phone 
        WHEN NOT MATCHED BY Source THEN
            DELETE;
        END TRY
        BEGIN CATCH
            THROW
        END CATCH
        """
    )
    cursor_ER.execute(f'EXEC DimShippers_ETL;')


def populate_fact_orders_etl(cursor_ER):
    """
    Populate The Dim Region table from the Relational_Database
    """
    cursor_ER.execute(f"DROP PROCEDURE IF EXISTS fact_orders_etl;")
    cursor_ER.execute(f'ALTER TABLE FactOrders NOCHECK CONSTRAINT all;')
    cursor_ER.execute(
        f"""
        create procedure fact_orders_etl
        as
        insert into FactOrders
        select Orders.OrderID,customerkey,Employees.EmployeeID,CONVERT(INT, CAST (OrderDate as DATETIME)),CONVERT(INT, CAST (RequiredDate as DATETIME)),CONVERT(INT, CAST (ShippedDate as DATETIME)),ShipVia,Freight,ShipName,ShipAddress,ShipCity,ShipRegion,ShipPostalCode,ShipCountry,products.ProductID,products.UnitPrice,Quantity,Discount 
        from 
        Orders_RELATIONAL_DB.dbo.Region
        inner join Orders_RELATIONAL_DB.dbo.Territories ON  Orders_RELATIONAL_DB.dbo.Territories.RegionID =Orders_RELATIONAL_DB.dbo.Region.RegionID
        INNER JOIN Orders_RELATIONAL_DB.dbo.EmployeeTerritories ON Orders_RELATIONAL_DB.dbo.Territories.TerritoryID = Orders_RELATIONAL_DB.dbo.EmployeeTerritories.TerritoryID
        INNER JOIN Orders_RELATIONAL_DB.dbo.Employees ON Orders_RELATIONAL_DB.dbo.Employees.EmployeeID = Orders_RELATIONAL_DB.dbo.EmployeeTerritories.EmployeeID
        INNER JOIN Orders_RELATIONAL_DB.dbo.Orders ON Orders_RELATIONAL_DB.dbo.Employees.EmployeeID = Orders_RELATIONAL_DB.dbo.Orders.EmployeeID
        INNER JOIN Orders_RELATIONAL_DB.dbo.Shippers ON Orders_RELATIONAL_DB.dbo.Orders.ShipVia = Orders_RELATIONAL_DB.dbo.Shippers.ShipperID
        INNER JOIN Orders_RELATIONAL_DB.dbo.Customers ON Orders_RELATIONAL_DB.dbo.Orders.CustomerID = Orders_RELATIONAL_DB.dbo.Customers.CustomerID
        INNER JOIN Orders_RELATIONAL_DB.dbo.OrderDetails ON Orders_RELATIONAL_DB.dbo.Orders.OrderID = Orders_RELATIONAL_DB.dbo.OrderDetails.OrderID
        INNER JOIN Orders_RELATIONAL_DB.dbo.Products ON Orders_RELATIONAL_DB.dbo.OrderDetails.ProductID = Orders_RELATIONAL_DB.dbo.Products.ProductID
        INNER JOIN Orders_RELATIONAL_DB.dbo.Suppliers ON Orders_RELATIONAL_DB.dbo.Products.SupplierID = Orders_RELATIONAL_DB.dbo.Suppliers.SupplierID
        INNER JOIN Orders_RELATIONAL_DB.dbo.Categories ON Orders_RELATIONAL_DB.dbo.Products.CategoryID = Orders_RELATIONAL_DB.dbo.Categories.CategoryID
        INNER JOIN DimCustomers ON DimCustomers.CustomerID = Orders_RELATIONAL_DB.dbo.Customers.CustomerID;
        """
    )

    cursor_ER.execute(f'EXEC fact_orders_etl;')


def populate_dim_employee_etl(cursor_ER):
    """
    Populate The Dim Employees table from the Relational_Database
    """

    cursor_ER.execute(f'DROP PROCEDURE IF EXISTS DimEmployees_ETL;')
    cursor_ER.execute(
        """
        
        CREATE PROCEDURE DimEmployees_ETL
        AS
        BEGIN
          SET NOCOUNT ON;
        
          -- Insert new rows into DimEmployees table
          INSERT INTO DimEmployees (EmployeeID, LastName, FirstName, Title, TitleOfCourtesy, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Extension, Photo, Notes, ReportsTo, PhotoPath, EffectiveDate, CurrentIndicator)
          SELECT e.EmployeeID, e.LastName, e.FirstName, e.Title, e.TitleOfCourtesy, e.BirthDate, e.HireDate, e.Address, e.City, e.Region, e.PostalCode, e.Country, e.HomePhone, e.Extension, e.Photo, e.Notes, e.ReportsTo, e.PhotoPath, GETDATE(), 1
          FROM Orders_RELATIONAL_DB.dbo.Employees e
          WHERE NOT EXISTS (SELECT 1 FROM DimEmployees de WHERE de.EmployeeID = e.EmployeeID AND de.CurrentIndicator = 1);
        
          -- Update existing rows in DimEmployees table
          UPDATE de
          SET de.LastName = e.LastName,
              de.FirstName = e.FirstName,
              de.Title = e.Title,
              de.TitleOfCourtesy = e.TitleOfCourtesy,
              de.BirthDate = e.BirthDate,
              de.HireDate = e.HireDate,
              de.Address = e.Address,
              de.City = e.City,
              de.Region = e.Region,
              de.PostalCode = e.PostalCode,
              de.Country = e.Country,
              de.HomePhone = e.HomePhone,
              de.Extension = e.Extension,
              de.Photo = e.Photo,
              de.Notes = e.Notes,
              de.ReportsTo = e.ReportsTo,
              de.PhotoPath = e.PhotoPath,
              de.IneffectiveDate = GETDATE(),
              de.CurrentIndicator = 0
          FROM DimEmployees de
          INNER JOIN Orders_RELATIONAL_DB.dbo.Employees e ON e.EmployeeID = de.EmployeeID
          WHERE de.CurrentIndicator = 1;
        END
        """
    )
    cursor_ER.execute(f'EXEC DimEmployees_ETL;')


def populate_dim_customers_etl(cursor_ER):
    """
    Populate The Dim Territories table from the Relational_Database
    """

    cursor_ER.execute(f'DROP PROCEDURE IF EXISTS DimCustomers_ETL;')
    # cursor_ER.execute(f'ALTER TABLE BridgeEmployeeTerritories NOCHECK CONSTRAINT territory_id_fk;')

    cursor_ER.execute(
        """
                
        CREATE PROCEDURE DimCustomers_ETL
        AS
        BEGIN
              MERGE DimCustomers AS dc
              USING Orders_RELATIONAL_DB.dbo.Customers AS c
              ON c.CustomerID = dc.CustomerID
            
              WHEN MATCHED AND dc.Address <> c.Address THEN
                UPDATE SET Address = c.Address,
                           Address_prev_1 = dc.Address,
                           Address_prev_2 = dc.Address_prev_1,
                           CompanyName = c.CompanyName,
                           ContactName = c.ContactName,
                           ContactTitle = c.ContactTitle,
                           City = c.City,
                           Region = c.Region,
                           PostalCode = c.PostalCode,
                           Country = c.Country,
                           Phone = c.Phone,
                           Fax = c.Fax
            
              WHEN NOT MATCHED THEN
                INSERT (CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax)
                VALUES (c.CustomerID, c.CompanyName, c.ContactName, c.ContactTitle, c.Address, c.City, c.Region, c.PostalCode, c.Country, c.Phone, c.Fax);
            END;
                """
    )
    cursor_ER.execute(f'EXEC DimCustomers_ETL;')


def populate_products_etl(cursor_ER):
    """
    Populate The Dim Region table from the Relational_Database
    """
    cursor_ER.execute(f"DROP PROCEDURE IF EXISTS IngestProductsData;")
    cursor_ER.execute(
        f"""
      
    CREATE PROCEDURE IngestProductsData
    (
      @ProductID INT,
      @ProductName NVARCHAR(40),
      @SupplierID INT,
      @CategoryID INT,
      @QuantityPerUnit NVARCHAR(20),
      @UnitPrice MONEY,
      @UnitsInStock SMALLINT,
      @UnitsOnOrder SMALLINT,
      @ReorderLevel SMALLINT,
      @Discontinued BIT
    )
    AS
    BEGIN
      BEGIN TRANSACTION
      INSERT INTO DimProducts_History (QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued, SupplierCompanyName, SupplierContactTitle, SupplierContactName, SupplierCity, SupplierRegion, SupplierCountry, SupplierPostalCode)
      SELECT QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued, CompanyName, ContactTitle, ContactName, City, Region, Country, PostalCode
      FROM Orders_RELATIONAL_DB.dbo.Products p
      JOIN Orders_RELATIONAL_DB.dbo.Suppliers s ON p.SupplierID = s.SupplierID
      WHERE p.ProductID = @ProductID
    
      INSERT INTO DimProducts (ProductID, ProductHistoryID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued, CategoryName, CategoryDescription, SupplierCompanyName, SupplierContactTitle, SupplierContactName, SupplierCity, SupplierRegion, SupplierCountry, SupplierPostalCode)
      SELECT @ProductID, SCOPE_IDENTITY(), @ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued, c.CategoryName, c.Description, CompanyName, ContactTitle, ContactName, City, Region, Country, PostalCode
      FROM Orders_RELATIONAL_DB.dbo.Products p
      JOIN Orders_RELATIONAL_DB.dbo.Suppliers s ON p.SupplierID = s.SupplierID
      JOIN Orders_RELATIONAL_DB.dbo.Categories c ON p.CategoryID = c.CategoryID
      WHERE p.ProductID = @ProductID
    
      COMMIT
    END

        """
    )

    cursor_ER.execute("""DECLARE @ProductID INT, @ProductName NVARCHAR(40), @SupplierID INT, @CategoryID INT, @QuantityPerUnit NVARCHAR(20), @UnitPrice MONEY, @UnitsInStock SMALLINT, @UnitsOnOrder SMALLINT, @ReorderLevel SMALLINT, @Discontinued BIT

                DECLARE products_cursor CURSOR FOR
                SELECT ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued
                FROM Orders_RELATIONAL_DB.dbo.Products
                
                OPEN products_cursor
                
                FETCH NEXT FROM products_cursor INTO @ProductID, @ProductName, @SupplierID, @CategoryID, @QuantityPerUnit, @UnitPrice, @UnitsInStock, @UnitsOnOrder, @ReorderLevel, @Discontinued
                
                WHILE @@FETCH_STATUS = 0
                BEGIN
                  EXEC IngestProductsData @ProductID, @ProductName, @SupplierID, @CategoryID, @QuantityPerUnit, @UnitPrice, @UnitsInStock, @UnitsOnOrder, @ReorderLevel, @Discontinued
                
                  FETCH NEXT FROM products_cursor INTO @ProductID, @ProductName, @SupplierID, @CategoryID, @QuantityPerUnit, @UnitPrice, @UnitsInStock, @UnitsOnOrder, @ReorderLevel, @Discontinued
                END
                
                CLOSE products_cursor
                DEALLOCATE products_cursor;
                """)


def populate_dim_date_etl(cursor_ER):
    """
    Populate The Date table from the Relational_Database
    """

    cursor_ER.execute(f'drop procedure if exists fill_dimdate;')
    cursor_ER.execute(f'set identity_insert date on;')

    cursor_ER.execute(
        """
        create procedure fill_dimdate (@start_date DATE,@end_date DATE)
        as 
        begin try
        DECLARE @LoopDate datetime
        SET @LoopDate = @start_date

        WHILE @LoopDate <= @end_date
        BEGIN
         -- add a record into the date dimension table for this date
         INSERT INTO Date(datekey,date,day,Month,Quarter,Year,MonthName,WeekOfYear,WeekOfMonth,DayOfMonth,DayOfYear) VALUES (
            Year(@LoopDate) * 10000 +  Month(@LoopDate) * 100 + Day(@LoopDate)
            ,@LoopDate
            ,Day(@LoopDate)
            ,Month(@LoopDate),
            CASE WHEN Month(@LoopDate) IN (1, 2, 3) THEN 1
                WHEN Month(@LoopDate) IN (4, 5, 6) THEN 2
                WHEN Month(@LoopDate) IN (7, 8, 9) THEN 3
                WHEN Month(@LoopDate) IN (10, 11, 12) THEN 4 end, 
            Year(@LoopDate),
            Datename(m,@LoopDate),
            DATEPART(week, @LoopDate),
            (DATEPART(day,@LoopDate)-1)/7 + 1,
            day(@LoopDate),
            DATEPART (dayofyear , @LoopDate)
        )
         SET @LoopDate = DateAdd(d, 1, @LoopDate)
         END
        END TRY
        BEGIN CATCH
            THROW
        END CATCH;
                """
    )
    cursor_ER.execute(f"exec fill_dimdate @start_date='1950-01-01',@end_date='2022-05-20';")
    cursor_ER.execute(f"set identity_insert date off;")


def populate_dimensional(db='Orders_DIMENSIONAL_DW'):
    c_ER = readconfig.get_sql_config(r'sql_server_config.cfg', "Database1")
    # Create a connection string for SQL Server
    conn_info_ER = 'Driver={};Server={};Database={};Trusted_Connection={};UID={};PWD={};'.format(*c_ER)
    # Connect to the server and to the desired database
    conn_ER = pyodbc.connect(conn_info_ER)
    # Create a Cursor class instance for executing T-SQL statements
    cursor_ER = conn_ER.cursor()

    cursor_ER.execute(f"use {db}")

    populate_dim_shippers_etl(cursor_ER)
    populate_dim_employee_etl(cursor_ER)
    populate_products_etl(cursor_ER)
    populate_dim_customers_etl(cursor_ER)
    populate_dim_date_etl(cursor_ER)
    populate_fact_orders_etl(cursor_ER)

    cursor_ER.commit()
    cursor_ER.close()
    conn_ER.close()


if __name__ == '__main__':
    populate_dimensional()
