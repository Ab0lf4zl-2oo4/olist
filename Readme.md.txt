E-Commerce Data Warehouse & BI Platform

An end-to-end e-commerce analytics project built with Python, Microsoft SQL Server, T-SQL, Power BI, and FastAPI, using the Brazilian E-Commerce Public Dataset by Olist.

The project covers data profiling, SQL Server database design, data loading, data quality monitoring, scheduled validation, business intelligence reporting, and API-based access to data quality and system information.

Project Overview

The objective of this project is to transform raw e-commerce datasets into a structured SQL Server environment, develop reusable data quality checks, build an interactive management dashboard, and expose selected monitoring information through a REST API.

The workflow starts with Python-based data profiling and validation. The datasets are then loaded into a custom-designed SQL Server database, where relational constraints and stored procedures support data integrity and recurring quality checks.

Power BI provides business-oriented analysis of sales, products, categories, customers, and geographic patterns, while FastAPI exposes selected database and data quality information through API endpoints.

Technology Stack

- Python: Data profiling, initial validation, data loading, and API development
- Pandas: Dataset inspection and data quality analysis
- Microsoft SQL Server: Relational database and data warehouse environment
- T-SQL: Database objects, constraints, stored procedures, and data quality logic
- SQL Server Agent: Scheduled execution of data quality checks
- Power BI Desktop: Data modeling, DAX measures, and interactive dashboards
- FastAPI: REST API for data quality reporting and system monitoring

Project Workflow

1. Data profiling: Inspect the source CSV datasets using Python and Pandas to assess their structure, completeness, key fields, and potential data quality issues.
2. Database design: Create the SQL Server database and organize the source tables within the staging schema.
3. Data loading: Transfer the profiled datasets from Python into SQL Server.
4. Relational integrity: Define primary keys, foreign keys, identity columns where appropriate, and a composite primary key for order items.
5. Data quality monitoring: Implement a logging table and stored procedure-based checks to record validation results.
6. Scheduled execution: Configure a SQL Server Agent job to execute the data quality procedure weekly.
7. Business intelligence: Build a Power BI data model and management dashboard for sales and customer analytics.
8. API development: Use FastAPI to expose selected data quality results, database metadata, and connection status.

SQL Server and Data Quality

The SQL Server component establishes the relational database foundation for the project.

It includes:

- A custom SQL Server database named "ecommerce_dw".
- A staging layer containing the source datasets.
- Primary and foreign key constraints to represent relationships between entities.
- Identity-based surrogate identifiers where appropriate.
- A composite primary key for the "order_items" table, using "order_id" and "order_item_id".
- A centralized data quality logging table: "dbo.DataQualityLog".
- A stored procedure: "dbo.usp_RunDataQualityChecks".
- A SQL Server Agent job configured for recurring data quality validation.

Data Quality Logging

The "dbo.DataQualityLog" table stores the results of individual validation checks, including the execution identifier, check name, affected table, number of flagged rows, status, details, and execution timestamp.

The stored procedure evaluates multiple data quality rules, including:

- Duplicate identifier checks.
- Orders without matching customers.
- Invalid customer ZIP code prefixes.
- Unrecognized order statuses.
- Chronological consistency of order dates.
- Negative item prices and freight values.
- Negative product measurements.
- Invalid review scores.
- Duplicate category names.
- Zero-value payments requiring investigation.

The checks distinguish between successful validations, failed validations, and cases requiring further review.

The SQL Server A

gent job is configured to run the procedure every Friday at 6:00 AM, allowing the checks to be repeated without manually initiating each execution.

«Note: The scheduled execution time depends on the SQL Server Agent environment and its local time configuration.»

Power BI Management Dashboard

Power BI Desktop is used to develop an interactive management dashboard focused on commercial performance and customer behavior.

The analytical model includes the relationships required by the dashboard, together with relevant DAX measures, calculated columns where appropriate, and visualizations.

The dashboard covers:

- Sales performance: Revenue and sales volume analyzed at daily, monthly, and yearly levels.
- Product performance: Best-selling products ranked by sales volume and revenue.
- Category analysis: Category-level performance and comparisons.
- Customer segmentation: Analysis of customer groups and purchasing behavior.
- Geographic analysis: City-level sales patterns and customer or product preferences.
- Management reporting: Visual summaries designed to support business performance monitoring and decision-making.

The dashboard is intended to provide a consolidated view of sales trends, product performance, customer segments, and geographic patterns.

FastAPI Monitoring Interface

FastAPI provides an API layer for accessing selected information from the SQL Server environment.

The Python API component supports monitoring and reporting functionality related to:

- Data quality check results.
- Database table and column information.
- Database connectivity status.
- API health and availability.

This separates selected monitoring operations from direct database management and provides a structured interface for retrieving operational information.

The API is designed to run in the local development environment.

Repository Structure

The project is organized around six principal files:

File| Responsibility
"01_database_and_etl.sql"| SQL Server database objects, relational constraints, and SQL-based data operations included in the script
"02_sql_agent_job.sql"| SQL Server Agent job, execution step, and scheduling configuration
"03_data_profiling_and_loading.py"| Initial data quality profiling, database connectivity, and loading datasets into SQL Server
"04_power_bi_dashboard.pbix"| Power BI data model, DAX calculations, and management dashboard
"05_fastapi_app.py"| API endpoints for data quality reporting, database metadata, and connectivity monitoring
"README.md"| Project documentation, architecture, workflow, and setup guidance

The filenames above are illustrative. They should be aligned with the actual filenames in the repository. If database creation, data loading, and stored procedures are maintained in separate scripts, document each script accordingly.

Dataset

This project uses the Brazilian E-Commerce Public Dataset by Olist.

The source data contains multiple related datasets covering customers, orders, order items, payments, reviews, products, sellers, and product category translations.

The source CSV files are profiled in Python before being loaded into SQL Server.

The initial assessment did not indicate a need for extensive data transformation. The project therefore focuses on validating the source data, establishing a relational database structure, monitoring data quality, and enabling business analysis.

Getting Started

Prerequisites

- Python and the required project dependencies.
- Microsoft SQL Server.
- SQL Server Management Studio (SSMS) or another compatible SQL Server management client.
- SQL Server Agent, where supported and enabled by the SQL Server edition and configuration.
- Power BI Desktop.
- The Olist source dataset.

Setup Overview

1. Download the source dataset and place the CSV files in the configured project data directory.
2. Configure the SQL Server connection and database settings for your environment.
3. Execute the database creation and schema scripts in the documented order.
4. Run the Python profiling and data loading process.
5. Create the stored procedures and support

ing data quality objects.
6. Configure the SQL Server Agent job and verify its schedule.
7. Open the Power BI report and configure its data source connection.
8. Configure the FastAPI application's environment and database connection before starting the API.

Database paths, connection settings, and other machine-specific configuration must be adapted to the target environment.

Project Goals

This project demonstrates practical experience with:

- Python-based data profiling and validation.
- SQL Server database design and relational integrity.
- T-SQL stored procedures and data quality logging.
- Scheduled database monitoring with SQL Server Agent.
- Power BI data modeling, DAX, and business intelligence reporting.
- REST API development with FastAPI.
- Integration between Python, SQL Server, and Power BI.

The overall goal is to demonstrate how data profiling, relational database design, recurring quality checks, analytical reporting, and API-based monitoring can work together within an e-commerce analytics solution.