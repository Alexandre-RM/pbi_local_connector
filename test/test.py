import pbi_local_connector as pbi

reportId, reportPort = pbi.getReportInfo()
df = pbi.getTableFromReport("MyTableName")