from sys import path
import os
import logging
import pandas as pd

def __initADOMD():
    try:
        adomdPath = f"\\Program Files\\Microsoft.NET\\ADOMD.NET\\{next(os.walk("C:\\Program Files\\Microsoft.NET\\ADOMD.NET"))[1][0]}"
        
        path.append(adomdPath)
        from pyadomd import Pyadomd

        logging.info("ADOMD library found and imported.")
    except:
        logging.error("ADOMD library not  found. You MUST install it from either : \n \
                    https://go.microsoft.com/fwlink/?linkid=829577\n \
                    https://learn.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions")
    

# need manual installation of ADOMD available at 
# https://learn.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions
# or direct install at
# https://go.microsoft.com/fwlink/?linkid=829577

__initADOMD()
from pyadomd import Pyadomd



def getReportInfo() -> tuple[str, str]:
    """
    Return a tuple containing (reportId, reportPort)
    """

    path1 = os.environ['LocalAppData'] + r"\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces"
    path2 = os.environ['userprofile'] + r"\Microsoft\Power BI Desktop Store App\AnalysisServicesWorkspaces"
    pbiPath = None

    if os.path.isdir(path1):
        pbiPath = path1
    elif os.path.isdir(path2):
        pbiPath = path2
    
    if pbiPath == None:
        logging.error("Please open a report in PowerBI desktop.")
    else:
        logging.info("PowerBI report well detected.")
    
    subFolders = next(os.walk(pbiPath))[1]
    
    if len(subFolders) > 1:
        logging.warning("More than one report is opened. One will be picked up randomly. To avoid this, close all reports but one.")

    pbiPath += "\\" + subFolders[0] + "\\Data\\"

    with open(pbiPath + "msmdsrv.port.txt", mode="r") as f:
        reportPort = f.readline().encode('latin-1').decode('utf-16')
        f.close()

    reportId:str = [bddId.split(".1.db.xml")[0] for bddId in os.listdir(pbiPath) if bddId.endswith(".1.db.xml")][0]
    return (reportId, "localhost:" + reportPort)


def getTableFromReport(tableName:str) -> pd.DataFrame:
    """Get a table from PowerBI dataset as pd DataFrame
    \nReport must be manually opened!

    Args:
        tableName (str): table name to get

    Returns:
        pd.DataFrame: table
    """  

    reportId, reportPort = getReportInfo()

    conn_str = f'Provider=MSOLAP;Data Source={reportPort};Catalog={reportId};'
    query = f"""EVALUATE {tableName}"""

    with Pyadomd(conn_str) as conn:
        with conn.cursor().execute(query) as cur:
            df = pd.DataFrame(cur.fetchone(), 
                              columns=[i.name.replace(f"{tableName}[", "").replace("]", "") for i in cur.description])
            
            print(cur.description)

    return df