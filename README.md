**Overview:**

Project based on [**pyadomd**](https://pypi.org/project/pyadomd/), thank you [**SCOUTsoftware**](https://pypi.org/user/SCOUTsoftware/).

It aims to connect simply to any locally opened PowerBI dashboard, and export data from it.

Data is provided as a pandas DataFrame.


**Usage examples:**

Get data from a table in the PowerBI report:

```
import pbi_local_connector as pbi

df = pbi.getTableFromReport("MyTableName")
```

You can also get report id and report port using the following:

```
import pbi_local_connector as pbi

reportId, reportPort = pbi.getReportInfo()
```



**Known limits:**

- Only 1 PowerBI dashboard must be opened, otherwise it can causes inconsistencies,
- ADOMD library must be manually installed from [ms source](https://learn.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions).
