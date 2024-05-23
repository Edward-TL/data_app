# data_app
 Make queries, clean data, save the tables and create plots. It follows the ETL classic flow as the modules indicates

# Extract
It refers, in general terms, to the db connection, but due to a Spark Data Base, managed with binary and flat text files, the concept of "connection" doesn't work like that. 

The types of db connections that can be found are:

1. **SQL**: Using SQL alchemy for MySQL database.
2. **REST API**: Requires:
   1. WIX Site:
      * Authentication Token.
      * Account ID
      * Site ID
3. **Spark**: For NoSQL data base that uses files. For eficiency in times, it's better to generate the parquet file, so the load and query times are reduced, as the size itself.

All permisions must be stored on a .env file according to the type. If the file stores the api keys, so the file must be `rest_api.env`, it there is a PostgreSQL or MySQL, then `sql.env`, etc.

## query_objects
Here goes all the query made by an ORM or a Query Maker, where a query has to be done due to its complexity or permissions.

Remember that ORM queries must be functions, meanwhile queries made by the Query Maker are based on the objects of this tool.

# transform
Here the transformations required for a job are stored as a python script. In order to this works right, every script must have a `clean` function (that works as `main` but helps with the sintaxis when its called), where it must receive only the **dirty data** and returns the data in the structured needed. For example:

```python
from extract import sql
from transform import sells_report

dirty_data = sql.get(query)

sells_data = sells_report.clean(dirty_data)

```

Another way to manage it, is with the storage of the processes made on a script and call them by calling this module.

```python
from extract import sql
from transform import reports 

dirty_data = sql.get(query)

sells_data = reports.sells.clean(dirty_data)

```

# load
Loads and saves the files in the way the user needs:
* Excel
* CSV
* Parquet
* DB Table

# Reporter
Creates the report on the tool needed.
* Excel using openpyxl
* Plotly using graph objects

Minimum requires to set Palette. For every tool used, first you must call the Plot Object, setting from the start the type of it by the object used. If you decide, you could pass a list of the graphs that you need, so they will be generated and called instead everytime you need it. Preseted values are `plotly` and `excel`, so you can check the plot on a jupyter notebook before you send it to an excel file, by using the common .show().

```python
from reporter.plots import Pie, Bar, Line

month_sells = Line(data, layout, types = ['plotly', 'excel'])
group_sells = Pie(data, layout)
quarter_sells = Bar(data, layout)

motnh_sells.show()
```
