# BI Final Project 
The current project was made for final group project for the course DS206 at the American University of Armenia.\
Instructor: Arman Asryan \
Contributors: \
[Lusine Babayan](mailto:lusine_babayan@edu.aua.am) \
[Gegham Harutyunyan](mailto:gegham_harutyunyan@edu.aua.am) \
[Elina Israyelyan](mailto:elina_israyelyan@edu.aua.am)


#### Requirements
To run the `xlsx_to_sql_ingest.py`  file you need to install the following packages:
* pandas
* pyodbc
* numpy 
* openpyxl
* configparser 



Also, you will need file `sql_server_config.cfg` with the following content
```
[Database1]
Driver={ODBC DRIVER NAME}
Server={Server name}
Database={Database name}
Trusted_Connection={yes/no}
User={username}
Password={password}
```