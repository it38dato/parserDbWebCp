from lib2to3.btm_utils import reduce_tree
from scripts.importKeysJson import funcLoadConfig, CONFIG_FILE_PATH
from scripts.importSqlToPandas import funcImportSqlToPandas, funcImportSqlToPandas2
from scripts.importDataFromSite import funcPowerDrivaer, funcFindAndClickObjectSite, funcFindObjectsSite, funcFindFilterClick2ObjectSite, funcFindFilterClick1ObjectSite, funcClick1ObjectSite, funcClickAlert1ObjectSite, funcFindObjectSite, funcCloseWindow, funcSearchBrowser, funcFindTableClick, funcFindTableClick2, funcFimdMenuClick, funcFindFornmFilterInputValue
from scripts.jobStings import funcImportStrToList, funcDiffStringsAddList
from scripts.jobDf import funcImport2listsToDf, funcGetSuffRenameColDf, funcFindNeighbour, funcJoin2Df, funcGet1DfFrom2Lists, funcJoin3df, funcJoin2Df2
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv

CONFIG_DATA = funcLoadConfig(CONFIG_FILE_PATH)
#print(CONFIG_DATA)
load_dotenv()
strPces = os.environ.get("P1")
strPbars = os.environ.get("P2")
strAcesNokia = os.environ.get("A1")
strAcesEricsson = os.environ.get("A2")
strUces = os.environ.get("U1")
strUcesSite = os.environ.get("U2")
strDnetFolder = os.environ.get("D1")

def checkTable(check):
    return check.empty
'''def funcParsingRdb(browser, filterObjectSite):
    #print(filterObjectSite)

    listTegs, symbol, tegs = funcImportStrToList([], ", ", CONFIG_DATA.get("TEGSSITE1"))#p$body$ListSearch$listSearchBox, td.fieldType-eString a.Link, td.Value.FormTd"
    
    browser, tegSearch, tegCandidate, filterObjectSite = funcFindAndClickObjectSite(browser, listTegs[0], listTegs[1], filterObjectSite)
    print(browser)
    print(tegSearch)
    print(tegCandidate)
    print(filterObjectSite)

    browser, teg, findTd = funcFindObjectsSite(browser, listTegs[2], [])
    print(browser)
    print(teg)
    print(findTd)
    needData1 = findTd[1].text
    needData2 = findTd[13].text
    needData3 = findTd[15].text
    print(needData1)
    print(needData2)
    print(needData3)
    return needData1, needData2, needData3'''
def funcParsingBars(browser, filterObjectSite):
    print(f"+ Launch parsser website BARS")
    listTegs1 = CONFIG_DATA.get("TEGSSITE1")
    #print(f"+ Add list (listTegs1):\n {listTegs1}")
    #print(filterObjectSite)
    #print(listTegs1[0])
    browser, teg = funcCloseWindow(browser, listTegs1[0])
    #print(listTegs1[1])
    browser, teg, filterObjectSite = funcSearchBrowser(browser, listTegs1[1], filterObjectSite)
    #print(listTegs1[2])
    #print(listTegs1[3])
    #print(listTegs1[4])
    browser, tegTbody, tegTr, tegTdA = funcFindTableClick(browser, listTegs1[2], listTegs1[3], listTegs1[4])
    browser, tegTbody, tegTr, tegTdA = funcFindTableClick2(browser, listTegs1[5], listTegs1[6], listTegs1[7])
    #print(listTegs1[8])
    #print(listTegs1[9])
    browser, tegDivClick, tegDivInput = funcFimdMenuClick(browser, listTegs1[8], listTegs1[9])
    # Инициализируем плоский список
    listFindInputs = []
    #print(listTegs1[10])
    #print(listTegs1[11])
    browser, tegForm, tegInputDiv, listFindInputs = funcFindFornmFilterInputValue(browser, listTegs1[10], listTegs1[11], listFindInputs)
    needData1 = listFindInputs[2]
    needData2 = listFindInputs[5]
    needData3 = listFindInputs[6]
    print(f"+ Finish parser website BARS. Get data from BARS (UCN - {needData1}, Latitude X1 - {needData2}, Longitude - Y1 {needData3}) and DB Physcical Parameters (X2, Y2):")
    #print(needData1)
    #print(needData2)
    #print(needData3)
    return needData1, needData2, needData3
def funcAddDfTemplateUcn(df):
    dictLac = {"BU":10340, "VV":52412, "IR":5370, "BI":40004, "HB":32106, "ZB":53711, "AM":54500, "YA":57641, "KM":37406, "MD":38718, "SA":38005, "AN":40701}
    dictBsc = {"BU":"-", "VV":"-", "IR":"IRK484", "BI":"BIR067", "HB":"KHB173", "ZB":"PRM140", "AM":"PRM140", "YA":"NSK042", "KM":"KAM070", "MD":"-", "SA":"-", "AN":"-"}
    dictRac = {10340:0, 52412:0, 5370:228, 40004:228, 32106:116, 53711:0, 54500:0, 57641:228, 37406:228, 38718:228, 38005:228, 40701:228}
    dfLac = pd.DataFrame(list(dictLac.items()), columns=["RegUcn", "LAC"])
    dfBsc = pd.DataFrame(list(dictBsc.items()), columns=["RegUcn", "BSC"])
    dfRac = pd.DataFrame(list(dictRac.items()), columns=["LAC", "RAC"])
    ucnLBTable = pd.merge(dfLac, dfBsc, left_on="RegUcn", right_on="RegUcn", how="outer")
    df = pd.merge(ucnLBTable, dfRac, left_on="LAC", right_on="LAC", how="outer") 
    return df
def funcAddDfTemplateUcnBulat(df):
    dictLac = {"BU":10351, "VV":52421, "IR":5381, "BI":40011, "HB":32112, "ZB":53714, "AM":54503, "YA":57644}
    dictBsc = {"IR":"BSCB-IRK525-1", "HB":"BSCB-KHB576-1", "YA":"BSCB-YAK558-1", "AM":"BSCB-BLG514-1", "BI":"BSCB-BIR522-1", "ZB":"BSCB-CHI523-1", "VV":"BSCB-VLD547-1", "BU":"BSCB-BRT551-1"}
    dictRac = {54503:14, 40011:54, 53714:23, 5381:54, 52421:47, 10351:51, 57644:54, 32112:54}
    dfLac = pd.DataFrame(list(dictLac.items()), columns=["RegUcn", "LAC"])
    dfBsc = pd.DataFrame(list(dictBsc.items()), columns=["RegUcn", "BSC"])
    dfRac = pd.DataFrame(list(dictRac.items()), columns=["LAC", "RAC"])
    #dfLac = pd.DataFrame(list(dictLac.items()), columns=['RegUcn', 'LacUcn'])
    #dfBsc = pd.DataFrame(list(dictBsc.items()), columns=['RegUcn', 'BscUcn'])
    #dfRac = pd.DataFrame(list(dictRac.items()), columns=['LacUcn', 'RacUcn'])
    ucnLBTable = pd.merge(dfLac, dfBsc, left_on='RegUcn', right_on='RegUcn', how='outer')
    df = pd.merge(ucnLBTable, dfRac, left_on="LAC", right_on="LAC", how="outer")
    #df = pd.merge(ucnLBTable, dfRac, left_on='LacUcn', right_on='LacUcn', how='outer')
    return df
def funcParsingCes(browser, filterObjectSite):
    print(f"+ Launch parser website CreateSite")
    listTegs, symbol, tegs = funcImportStrToList([], ", ", filterObjectSite)
    #print(listTegs)
    browser.maximize_window()
    browser, tegUsername, tegPasswd, click, username, passwd = funcFindFilterClick2ObjectSite(browser, listTegs[0], listTegs[1], listTegs[2], strUcesSite, strPbars)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, listTegs[3])))
    browser, tegBsslink = funcClick1ObjectSite(browser, listTegs[3])
    browser, tegTecnoklogylink = funcClick1ObjectSite(browser, listTegs[4])
    browser, tegImportlink = funcClickAlert1ObjectSite(browser, listTegs[5])
    #print(file)
    #print(os.getcwd()+"\\"+file)
    browser, tegPublicationFile, click, filterFile = funcFindFilterClick1ObjectSite(browser, listTegs[6], listTegs[2], os.getcwd()+"\\"+file)
    time.sleep(5)
    browser, tegClass, findHtmlMessage = funcFindObjectSite(browser, listTegs[7], "")
    if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
        print("- Attention! The file "+file+" for import does not match.")
    if "Импорт выполнен" in str(findHtmlMessage[0]):
        if "КРОМЕ" in str(findHtmlMessage[0]):
            print("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.")
        else:
            print("+ Import file "+file+" completed successfully.")
    print(f"+ Finish parser website CreateSite")
    return

df2gNok, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesNokia, strUces, strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY1")
)
df3gNok, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesNokia, strUces, strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY2")
)
df4gNok, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesNokia, strUces, strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY3")
)
df2gNokBul, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesNokia, strUces, strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY4")
)
df4gNokBul, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesNokia, strUces, strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY5")
)
df2gEr, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesEricsson,strUces,strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY6")
)
df3gEr, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesEricsson,strUces,strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY7")
)
df4gEr, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesEricsson,strUces,strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY8")
)
df2gErBul, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesEricsson,strUces,strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY9")
)
df4gErBul, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(),strAcesEricsson,strUces,strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY10")
)
df2gErBulNeop, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesEricsson,strUces,strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY11")
)
df4gErBulNeop, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
    pd.DataFrame(), strAcesEricsson,strUces,strPces,"CreateSite", CONFIG_DATA.get("DBQUERRY12")
)

listNameNewBs = []
listReady = []
listData = []
#df2gNok["Reg"] = ["IR", "IR"]
#df2gNok["BS_name"] =["IO0265", "IR1159"]
#df2gNok["BCF"] = ["0265", "1159"]
#df2gNok["Sector"] = ["IO02651", "IR11592"]

if checkTable(df2gNok) == False:
    print(f"+ Add Empty table (df2gNok):\n{df2gNok}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all",CONFIG_DATA.get("DBQUERRY13")
    )
    #print(dfDaily)
    dfOld = pd.merge(df2gNok, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")    
    #print(f"+ Add table (dfOld):\n{dfOld}")

    #listTech = df2gNok["BS_name"].tolist()
    #listTech = list(dict.fromkeys(listTech))
    #listTechOld = dfOld["BS_name"].tolist()
    #listTechOld = list(dict.fromkeys(listTechOld))
    #for name in listTech:
    #    if name in listTechOld:
    #        continue
    #    else:
    #        listNameNewBs.append(name)
    #listNameNewBs.append("IO0265")
    #listNameNewBs.append("IR0045")
    #dfNameNewBs = pd.DataFrame(listNameNewBs, columns=["nameNew"])
    dfNameNewBs, df2gNok, dfOld, listNameNewBs, str2gNokCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gNok, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb=0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb=numb+1
                #print(str(numb)+". The site "+name+" is being read:")                
                findUcn, findLatitude, findLongitude  = funcPowerDrivaer(
                    #driver_path = CONFIG_DATA.get("LINKPO1"),
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path = CONFIG_DATA.get("LINKPO2"),
                    url = CONFIG_DATA.get("LINKSITE1"),
                    action_func = funcParsingBars,
                    filterObjectSite = name[:2] + "00"+ name[2:6]
                )
                #print(findUcn)
                #print(findLatitude)
                #print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН", "УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.')) 
                listReady.append(name)
        #print(listData)
        #print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        #print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index", "RegUcn", "IO", "IR", 2
        )
        #print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        #print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        #print("dfDaily:")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df2gNok, dfDaily, strNoUcn, str2gNok = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gNok, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            # print(f"+ Correct table (dfNoUcn):\n{dfNoUcn.to_string()}")
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols2gNok(dfNoUcn)
            dfNoUcn["BCF"] = dfNoUcn["BCF"].astype("int64")
            dfNoUcn["SW"] = "MR10"
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
            #dfNoUcn = dfNoUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC", "BS_name"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print("dfNoUcn:")
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df2gNok, dfUcnTemplate, strUcn1, strUcn2, str2gNok, strUcnTemplate  = funcJoin2Df2(
                dfUcn, df2gNok, dfUcnTemplate,"index", "RegUcn", "BS_name", "RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            #dfUcn = funcCorrectCols2gNok(dfUcn)
            dfUcn["BCF"] = dfUcn["BCF"].astype("int64")
            dfUcn["SW"] = "MR10"
            dfUcn = dfUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
            #dfUcn = dfUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC", "BS_name"])
            dfNew = pd.concat([dfNew, dfUcn])
        #print("dfUcn:")
        #print(dfUcn)
    #print(f"+ Correct table (dfNew):\n{dfNew}")

    if checkTable(dfNew) == False:
        print(f"- Need check code after table (dfNew)")
        dfNew["BS_name"] = dfNew["Sector"].str[:6]
        dfCheckLac = dfNew.groupby("BS_name")["LAC"].transform("nunique")  # Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfNew[~(dfCheckLac >= 2)]  # Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfNew[dfCheckLac >= 2]  # Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        dfUnCorrect["BS_name"] = dfUnCorrect["BS_name"].astype(str)# добавил из-за ошибки: ValueError: You are trying to merge on object and float64 columns for key 'BS_name'. If you wish to proceed you should use pd.concat
        dfNewAndNeighbourBS["BS_name_x"] = dfNewAndNeighbourBS["BS_name_x"].astype(str)# добавил из-за ошибки: ValueError: You are trying to merge on object and float64 columns for key 'BS_name'. If you wish to proceed you should use pd.concat
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.reindex(columns=["BS_name_x", "BS_name_y"])
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.drop_duplicates()
        #print(f"+ Correct table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfNewAndNeighbourBS, left_on="BS_name", right_on="BS_name_x", how="inner")
        # print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1  # Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name_y"] + dfUnCorrect["BS_Id"].astype(str)
        # print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(), strAcesNokia, strUces, strPces,"Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        # print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        # print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        dfUnCorrect = dfUnCorrect.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
        dfCorrect = dfCorrect.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
        # print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfNew, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        # print(f"+ Correct table (dfNew):\n{dfNew}"
    if checkTable(dfOld) == False:
        dfCheckLac = dfOld.groupby("BS_name")["LAC"].transform("nunique")# Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfOld[~(dfCheckLac >= 2)]# Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfOld[dfCheckLac >= 2]# Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        print(f"- Need check code for table (dfUnCorrect)")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1# Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name"] + dfUnCorrect["BS_Id"].astype(str)
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        #print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        if "RAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "RAC", dfUnCorrect["RAC_y"])
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfUnCorrect["SW"] = "MR10"
        dfUnCorrect["BCF"] = dfUnCorrect["BCF"].astype("int64")
        dfCorrect["SW"] = "MR10"
        dfCorrect["BCF"] = dfCorrect["BCF"].astype("int64")
        dfUnCorrect = dfUnCorrect.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
        dfCorrect = dfCorrect.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
        #print(f"+ Correct tables (dfUnCorrect,dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfOld, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        #print(f"+ Correct table (dfOld):\n{dfOld}")

    df2gNok, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df2gNok):\n{df2gNok}")
    df2gNok.to_csv("df2gNok.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")
    listFiles = os.listdir()
    #print(listFiles)
    #for file in listFiles:
    #    if "df2gNok." in file:
    #        #print(file)
    #        dataFromSite  = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path = CONFIG_DATA.get("LINKPO2"),
    #            url = CONFIG_DATA.get("LINKSITE2"),
    #            action_func = funcParsingCes,
    #            filterObjectSite = CONFIG_DATA.get("TEGSSITE2")
    #        )
    #        #print(dataFromSite)
    #        print("+ Add Data (df2gNok) to site CES")
if checkTable(df2gNokBul) == False:
    print(f"+ Add Empty table (df2gNokBul):\n{df2gNokBul}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY13")
    )
    #print(dfDaily)
    dfOld = pd.merge(df2gNokBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df2gNokBul, dfOld, listNameNewBs, str2gNokBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gNokBul, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН", "УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index", "RegUcn", "IO", "IR", 2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            print("- Внимание! Еще не было данных не УЦН по булату. необходимо проверить код ниже.")
            dfNeighbour, dfNoUcn, df2gNokBul, dfDaily, strNoUcn, str2gNokBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gNokBul, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            # print(f"+ Correct table (dfNoUcn):\n{dfNoUcn.to_string()}")
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols2gNok(dfNoUcn)
            dfNoUcn["BCF"] = dfNoUcn["BCF"].astype("int64")
            dfNoUcn["SW"] = "MR10"
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("- Внимание! В Булате отображается названия таблица не как в нокиа - LAC, RAC. Я заменил парамеетры в функции (funcAddDfTemplateUcnBulat) название колонок, но лучше перероверить.")
            dfUcn, df2gNokBul, dfUcnTemplate, strUcn1, strUcn2, str2gNokBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gNokBul, dfUcnTemplate,"index", "RegUcn", "BS_name", "RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            #dfUcn = funcCorrectCols2gNok(dfUcn)
            dfUcn["BCF"] = dfUcn["BCF"].astype("int64")
            dfUcn["SW"] = "MR10"
            dfUcn = dfUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    # print(dfNew)
    #dfOld = funcCorrectCols2gNok(dfOld)
    dfOld["BCF"] = dfOld["BCF"].astype("int64")
    dfOld["SW"] = "MR10"
    dfOld = dfOld.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
    #print(dfOld)

    df2gNokBul, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df2gNokBul):\n{df2gNokBul}")
    df2gNokBul.to_csv("df2gNokBul.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    #print(listFiles)
    #for file in listFiles:
    #    if "df2gNokBul." in file:
    #        #print(file)
    #        dataFromSite  = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path = CONFIG_DATA.get("LINKPO2"),
    #            url = CONFIG_DATA.get("LINKSITE2"),
    #            action_func = funcParsingCes,
    #            filterObjectSite = CONFIG_DATA.get("TEGSSITE2")
    #        )
    #        #print(dataFromSite)
    #        print("+ Add Data (df2gNokBul) to site CES")
if checkTable(df3gNok) == False:
    print(f"+ Add Empty table (df3gNok):\n{df3gNok}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all",CONFIG_DATA.get("DBQUERRY16")
    )
    #print(f"+ Add table (dfDaily):\n{dfDaily}")
    dfOld = pd.merge(df3gNok, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    # print(dfOld)

    dfNameNewBs, df3gNok, dfOld, listNameNewBs, str3gNokCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df3gNok, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    # print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН", "УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index", "RegUcn", "IO", "IR", 2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        #print(f"+ Add table (dfCoords):\n{dfCoords}")
        #dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="Namefor3g", right_on="BS_name", how="inner") # Поменял BS_name на Namefor3g, так как для БС IR2350 добавлял соседство BU0001
        #print(f"+ Correct table (dfDaily):\n{dfDaily}")
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        #print(f"+ Correct table (dfNoUcn):\n{dfNoUcn}")
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df3gNok, dfDaily, strNoUcn, str3gNok = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df3gNok, dfDaily,"index", "BS_name"
            )
            #print(f"+ Add table (dfNeighbour):\n{dfNeighbour}")
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            # print(f"+ Correct table (dfNoUcn):\n{dfNoUcn.to_string()}")
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #Убрал код ниже так как BS_name уже есть, а данный код как раз добавляет BS_name. необходимо проверить для других случаев, в том числе для довесов. так как там есть код, может его стоит убрать?
            #if "BS_name_x" in dfNoUcn:
            #    dfNoUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC", "RAC", "URA", "RNC_ID"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df3gNok, dfUcnTemplate, strUcn1, strUcn2, str3gNok, strUcnTemplate = funcJoin2Df2(
                dfUcn, df3gNok, dfUcnTemplate,"index", "RegUcn", "BS_name", "RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            #dfUcn = funcCorrectCols3gNok(dfUcn)
            if "BS_name_x" in dfUcn:
                dfUcn.insert(1, "BS_name", dfUcn["BS_name_x"])
            dfUcn = dfUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC", "RAC", "URA", "RNC_ID"])
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    # print(dfNew)

    print("- Need add code for correct different LAC/RAC/URA")
    #dfOld = funcCorrectCols3gNok(dfOld)
    if "BS_name_x" in dfOld:
        dfOld.insert(1, "BS_name", dfOld["BS_name_x"])
    dfOld = dfOld.reindex(columns=["Reg", "BS_name", "Sector", "LAC", "RAC", "URA", "RNC_ID"])
    #print(dfOld)

    df3gNok, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df3gNok):\n{df3gNok}")
    df3gNok.to_csv("df3gNok.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    #print(listFiles)
    #for file in listFiles:
    #    if "df3gNok." in file:
    #        #print(file)
    #        dataFromSite  = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path = CONFIG_DATA.get("LINKPO2"),
    #            url = CONFIG_DATA.get("LINKSITE2"),
    #            action_func = funcParsingCes,
    #            #filterObjectSite = ""
    #            filterObjectSite = CONFIG_DATA.get("TEGSSITE3")
    #        )
    #        #print(dataFromSite)
    #        print("+ Add Data (df3gNok) to site CES")
if checkTable(df4gNok) == False:
    print(f"+ Add Empty table (df4gNok):\n{df4gNok}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia, strUces, strPces,"Config_all", CONFIG_DATA.get("DBQUERRY17")
    )
    #print(f"+ Add table (dfDaily):\n{dfDaily}")
    dfOld = pd.merge(df4gNok, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(f"+ Add table (dfOld):\n{dfOld}")

    dfNameNewBs, df4gNok, dfOld, listNameNewBs, str4gNokCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gNok, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb=0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb=numb+1
                #print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude  = funcPowerDrivaer(
                    driver_path='\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path = CONFIG_DATA.get("LINKPO2"),
                    url = CONFIG_DATA.get("LINKSITE1"),
                    action_func = funcParsingBars,
                    filterObjectSite = name[:2] + "00"+ name[2:6]
                )
                #print(findUcn)
                #print(findLatitude)
                #print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН", "УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        #print(listData)
        #print(listReady)

        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        #print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index", "RegUcn", "IO", "IR", 2
        )
        #print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        #print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df4gNok, dfDaily, strNoUcn, str4gNok = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gNok, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            #print(f"+ Correct table (dfNoUcn):\n{dfNoUcn.to_string()}")
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols4gNok(dfNoUcn)
            if "BS_name_x" in dfNoUcn:
                dfNoUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("- Need Check table (dfUcn)")
            dfUcn, df4gNok, dfUcnTemplate, strUcn1, strUcn2, str4gNok, strUcnTemplate  = funcJoin2Df2(
                dfUcn, df4gNok, dfUcnTemplate,
                "index", "RegUcn", "BS_name", "RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            if "BS_name_x" in dfUcn:
                dfUcn.insert(1, "BS_name", dfUcn["BS_name_x"])
            dfUcn = dfUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
            #dfUcn = funcCorrectCols4gNok(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(f"+ Correct table (dfNew):\n{dfNew}")

    #dictTest = {
    #    'Reg': [
    #        'HB', 'HB', 'HB',
    #        'HB', 'HB', 'HB', 'HB', 'HB', 'HB',
    #        'HB', 'HB', 'HB', 'HB', 'HB', 'HB',
    #        'HB', 'HB', 'HB', 'HB', 'HB', 'HB'
    #    ],
    #    'BS_name': [
    #        'HB0894', 'HB0894', 'HB0894',
    #        'HB0504', 'HB0504', 'HB0504', 'HB0504', 'HB0504', 'HB0504',
    #        'HB0504', 'HB0504', 'HB0504', 'HB0504', 'HB0504', 'HB0504',
    #        'HB0504', 'HB0504', 'HB0504', 'HB0504', 'HB0504', 'HB0504'
    #    ],
    #    'Sector': [
    #        'HB0894_011', 'HB0894_012', 'HB0894_013',
    #        'HB0504_011', 'HB0504_011', 'HB0504_012', 'HB0504_012', 'HB0504_013', 'HB0504_013',
    #        'HB0504_014', 'HB0504_014', 'HB0504_015', 'HB0504_015', 'HB0504_016', 'HB0504_016',
    #        'HB0504_017', 'HB0504_017', 'HB0504_018', 'HB0504_018', 'HB0504_019', 'HB0504_019',
    #    ],
    #    'LAC': [
    #        32096, 32096, 32096,
    #        32099, 32102, 32099, 32102, 32099, 32102,
    #        32099, 32102, 32099, 32102, 32099, 32102,
    #        32099, 32102, 32099, 32102, 32099, 32102
    #    ]
    #}
    #dfTest = pd.DataFrame(dictTest)
    #print(f"+ Correct table (dfTest):\n{dfTest}")

    if checkTable(dfNew) == False:
        dfCheckLac = dfNew.groupby("BS_name")["LAC"].transform("nunique")  # Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfNew[~(dfCheckLac >= 2)]  # Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfNew[dfCheckLac >= 2]  # Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.reindex(columns=["BS_name_x", "BS_name_y"])
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.drop_duplicates()
        #print(f"+ Correct table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfNewAndNeighbourBS, left_on="BS_name", right_on="BS_name_x", how="inner")
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1  # Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name_y"] + dfUnCorrect["BS_Id"].astype(str)
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(), strAcesNokia,strUces,strPces, "Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        #print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        dfUnCorrect = dfUnCorrect.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfNew, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        #print(f"+ Correct table (dfNew):\n{dfNew}")
    # dfOld = funcCorrectCols4gNok(dfOld)
    if checkTable(dfOld) == False:
        if "BS_name_x" in dfOld:
            dfOld.insert(1, "BS_name", dfOld["BS_name_x"])
        dfOld = dfOld.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
        #print(f"+ Correct table (dfOld):\n{dfOld}")
        dfCheckLac = dfOld.groupby("BS_name")["LAC"].transform("nunique")# Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfOld[~(dfCheckLac >= 2)]# Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfOld[dfCheckLac >= 2]# Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1# Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name"] + dfUnCorrect["BS_Id"].astype(str)
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        #print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        # print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        dfUnCorrect = dfUnCorrect.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
        dfUnCorrect = dfUnCorrect.drop_duplicates()
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfOld, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        #print(f"+ Correct table (dfOld):\n{dfOld}")

    df4gNok, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df4gNok):\n{df4gNok}")
    df4gNok.to_csv("df4gNok.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    #print(listFiles)
    #for file in listFiles:
    #    if "df4gNok." in file:
    #        #print(file)
    #        dataFromSite  = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path = CONFIG_DATA.get("LINKPO2"),
    #            url = CONFIG_DATA.get("LINKSITE2"),
    #            action_func = funcParsingCes,
    #            #filterObjectSite = ""
    #            filterObjectSite = CONFIG_DATA.get("TEGSSITE3")
    #        )
    #        #print(dataFromSite)
    #        print("+ Import file (df4gNok) to site CES")
if checkTable(df4gNokBul) == False:
    print(f"+ Add Empty table (df4gNokBul):\n{df4gNokBul}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all",CONFIG_DATA.get("DBQUERRY17")
    )
    #print(dfDaily)
    dfOld = pd.merge(df4gNokBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df4gNokBul, dfOld, listNameNewBs, str4gNokBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gNokBul, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН", "УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)

        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index", "RegUcn", "IO", "IR", 2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        #print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df4gNokBul, dfDaily, strNoUcn, str4gNokBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gNokBul, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            #print(f"+ Correct table (dfNoUcn):\n{dfNoUcn.to_string()}")
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols4gNok(dfNoUcn)
            if "BS_name_x" in dfNoUcn:
                dfNoUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("Внимание! необходимо проверить заполнение данных таблицы dfUcn.")
            dfUcn, df4gNokBul, dfUcnTemplate, strUcn1, strUcn2, str4gNokBul, strUcnTemplate  = funcJoin2Df2(
                dfUcn, df4gNokBul, dfUcnTemplate,"index", "RegUcn", "BS_name", "RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            #dfUcn = funcCorrectCols4gNok(dfUcn)
            if "BS_name_x" in dfUcn:
                dfUcn.insert(1, "BS_name", dfUcn["BS_name_x"])
            dfUcn = dfUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    #dfOld = funcCorrectCols4gNok(dfOld)
    if "BS_name_x" in dfOld:
        dfOld.insert(1, "BS_name", dfOld["BS_name_x"])
    dfOld = dfOld.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
    #print(dfOld)

    df4gNokBul, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df4gNokBul):\n{df4gNokBul}")
    df4gNokBul.to_csv("df4gNokBul.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    #print(listFiles)
    #for file in listFiles:
    #    if "df4gNokBul." in file:
    #        #print(file)
    #        dataFromSite  = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path = CONFIG_DATA.get("LINKPO2"),
    #            url = CONFIG_DATA.get("LINKSITE2"),
    #            action_func = funcParsingCes,
    #            #filterObjectSite = ""
    #            filterObjectSite = CONFIG_DATA.get("TEGSSITE3")
    #        )
    #        #print(dataFromSite)
    #        print("+ Add Data (df4gNokBul) to site CES")
if checkTable(df2gEr) == False:
    print(f"+ Add Empty table (df2gEr):\n{df2gEr}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia, strUces, strPces,"Config_all", CONFIG_DATA.get("DBQUERRY13")
    )
    #print(dfDaily)
    dfOld = pd.merge(df2gEr, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df2gEr, dfOld, listNameNewBs, str2gErCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gEr, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("- Need check code after table (dfNameNewBs) ")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path='\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН","УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia, strUces, strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df2gEr, dfDaily, strNoUcn, str2gEr = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gEr, dfDaily, "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols2gEr(dfNoUcn)
            if "BS_name_x" in dfNoUcn:
                dfNoUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfNoUcn["TG"] = "0"
            dfNoUcn["SW"] = "-"
            dfNoUcn["RBL2_1"] = "-"
            dfNoUcn["RBL2_2"] = "-"
            dfNoUcn["OETM_1"] = "-"
            dfNoUcn["OETM_2"] = "-"
            if ("BscUcn" in dfNoUcn) and ("LacUcn" in dfNoUcn):
                dfNoUcn.insert(1, "BSC", dfUcn["BscUcn"])
                dfNoUcn.insert(1, "LAC", dfUcn["LacUcn"])
            dfNoUcn = dfNoUcn.reindex(columns=
                ["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2", "Sector"]
            )
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df2gEr, dfUcnTemplate, strUcn1, strUcn2, str2gEr, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gEr, dfUcnTemplate,"index","RegUcn","BS_name","RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            #dfUcn = funcCorrectCols2gEr(dfUcn)
            if "BS_name_x" in dfUcn:
                dfUcn.insert(1, "BS_name", dfUcn["BS_name_x"])
            dfUcn["TG"] = "0"
            dfUcn["SW"] = "-"
            dfUcn["RBL2_1"] = "-"
            dfUcn["RBL2_2"] = "-"
            dfUcn["OETM_1"] = "-"
            dfUcn["OETM_2"] = "-"
            if ("BscUcn" in dfUcn) and ("LacUcn" in dfNoUcn):
                dfUcn.insert(1, "BSC", dfUcn["BscUcn"])
                dfUcn.insert(1, "LAC", dfUcn["LacUcn"])
            dfUcn = dfUcn.reindex(columns=
                ["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2", "Sector"]
            )
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(f"+ Correct table dfNew:\n{dfNew}")

    if checkTable(dfNew) == False:
        #dfNew["BS_name"] = dfNew["site"].str[:6]
        dfCheckLac = dfNew.groupby("BS_name")["LAC"].transform("nunique")  # Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfNew[~(dfCheckLac >= 2)]  # Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfNew[dfCheckLac >= 2]  # Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.reindex(columns=["BS_name_x", "BS_name_y"])
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.drop_duplicates()
        #print(f"+ Correct table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS}")
        print(f"- Need check code for table (dfUnCorrect)")
        dfUnCorrect["BS_name"] = dfUnCorrect["BS_name"].astype(str)
        dfNewAndNeighbourBS["BS_name_x"] = dfNewAndNeighbourBS["BS_name_x"].astype(str)
        dfUnCorrect = pd.merge(dfUnCorrect, dfNewAndNeighbourBS, left_on="BS_name", right_on="BS_name_x", how="inner")
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1  # Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name_y"] + dfUnCorrect["BS_Id"].astype(str)
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(), strAcesNokia, strUces, strPces,"Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        #print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        dfUnCorrect = dfUnCorrect.reindex(columns=
            ["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2","Sector"]
        )
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfNew, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        #print(f"+ Correct table (dfNew):\n{dfNew}")
    #print(f"+ Correct table (dfOld):\n{dfOld}")
    if checkTable(dfOld) == False:
        print(f"- Need check code for table (dfOld)")
        dfCheckLac = dfOld.groupby("BS_name")["LAC"].transform("nunique")  # Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfOld[~(dfCheckLac >= 2)]  # Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfOld[dfCheckLac >= 2]  # Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1  # Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name"] + dfUnCorrect["BS_Id"].astype(str)
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(), strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        #print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        dfUnCorrect = dfUnCorrect.reindex(columns=["Reg", "BS_name", "Sector", "site", "LAC", "RAC", "BSC"])
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfOld, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        #print(f"+ Correct table (dfOld):\n{dfOld}")
    #dfOld = funcCorrectCols2gEr(dfOld)
    if "BS_name_x" in dfOld:
        dfOld.insert(1, "BS_name", dfOld["BS_name_x"])
    dfOld["TG"] = "0"
    dfOld["SW"] = "-"
    dfOld["RBL2_1"] = "-"
    dfOld["RBL2_2"] = "-"
    dfOld["OETM_1"] = "-"
    dfOld["OETM_2"] = "-"
    if ("BscUcn" in dfOld) and ("LacUcn" in dfOld):
        dfOld.insert(1, "BSC", dfUcn["BscUcn"])
        dfOld.insert(1, "LAC", dfUcn["LacUcn"])
    dfOld = dfOld.reindex(columns=["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2","Sector"])
    #print(f"+ Correct table (dfOld):\n{dfOld}")

    df2gEr, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df2gEr):\n{df2gEr}")
    df2gEr.to_csv("df2gEr.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    #print(listFiles)
    #for file in listFiles:
    #    if "df2gEr." in file:
    #        #print(file)
    #        dataFromSite  = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path = CONFIG_DATA.get("LINKPO2"),
    #            url = CONFIG_DATA.get("LINKSITE3"),
    #            action_func = funcParsingCes,
    #            filterObjectSite = CONFIG_DATA.get("TEGSSITE6")
    #        )
    #        #print(dataFromSite)
    #        print("+ Import file (df2gEr) to site CES")
if checkTable(df2gErBul) == False:
    print(f"+ Add Empty table (df2gErBul):\n{df2gErBul}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY13")
    )
    #print(dfDaily)
    dfOld = pd.merge(df2gErBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df2gErBul, dfOld, listNameNewBs, str2gErBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gErBul, dfOld, listNameNewBs, "BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print(f"- Need chack code after table (dfNameNewBs)")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН","УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df2gErBul, dfDaily, strNoUcn, str2gErBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gErBul, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols2gEr(dfNoUcn)
            if "BS_name_x" in dfNoUcn:
                dfNoUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfNoUcn["TG"] = "0"
            dfNoUcn["SW"] = "-"
            dfNoUcn["RBL2_1"] = "-"
            dfNoUcn["RBL2_2"] = "-"
            dfNoUcn["OETM_1"] = "-"
            dfNoUcn["OETM_2"] = "-"
            if ("BscUcn" in dfNoUcn) and ("LacUcn" in dfNoUcn):
                dfNoUcn.insert(1, "BSC", dfUcn["BscUcn"])
                dfNoUcn.insert(1, "LAC", dfUcn["LacUcn"])
            dfNoUcn = dfNoUcn.reindex(columns=
                ["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2","Sector"]
            )
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df2gErBul, dfUcnTemplate, strUcn1, strUcn2, str2gErBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gErBul, dfUcnTemplate,"index","RegUcn","BS_name","RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            # dfUcn = funcCorrectCols2gEr(dfUcn)
            if "BS_name_x" in dfUcn:
                dfUcn.insert(1, "BS_name", dfUcn["BS_name_x"])
            dfUcn["TG"] = "0"
            dfUcn["SW"] = "-"
            dfUcn["RBL2_1"] = "-"
            dfUcn["RBL2_2"] = "-"
            dfUcn["OETM_1"] = "-"
            dfUcn["OETM_2"] = "-"
            if ("BscUcn" in dfUcn) and ("LacUcn" in dfNoUcn):
                dfUcn.insert(1, "BSC", dfUcn["BscUcn"])
                dfUcn.insert(1, "LAC", dfUcn["LacUcn"])
            dfUcn = dfUcn.reindex(columns=
                ["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1","OETM_2", "Sector"]
            )
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(f"+ Correct table dfNew:\n{dfNew}")

    if "BS_name_x" in dfOld:
        dfOld.insert(1, "BS_name", dfOld["BS_name_x"])
    dfOld["TG"] = "0"
    dfOld["SW"] = "-"
    dfOld["RBL2_1"] = "-"
    dfOld["RBL2_2"] = "-"
    dfOld["OETM_1"] = "-"
    dfOld["OETM_2"] = "-"
    if ("BscUcn" in dfOld) and ("LacUcn" in dfOld):
        dfOld.insert(1, "BSC", dfUcn["BscUcn"])
        dfOld.insert(1, "LAC", dfUcn["LacUcn"])
    dfOld = dfOld.reindex(
        columns=["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2", "Sector"]
    )
    # print(f"+ Correct table (dfOld):\n{dfOld}")

    df2gErBul, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df2gErBul)\n{df2gErBul}")
    df2gErBul.to_csv("df2gErBul.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    #print(listFiles)
    #for file in listFiles:
    #    if "df2gErBul." in file:
    #        #print(file)
    #        dataFromSite  = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path = CONFIG_DATA.get("LINKPO2"),
    #            url = CONFIG_DATA.get("LINKSITE3"),
    #            action_func = funcParsingCes,
    #            filterObjectSite = CONFIG_DATA.get("TEGSSITE6")
    #        )
    #        #print(dataFromSite)
    #        print("+ Add Data (df2gErBul) to site CES")
if checkTable(df2gErBulNeop) == False:
    print(f"+ Add Empty table (df2gErBulNeop):\n{df2gErBulNeop}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY13")
    )
    # print(dfDaily)
    dfOld = pd.merge(df2gErBulNeop, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    # print(dfOld)

    dfNameNewBs, df2gErBulNeop, dfOld, listNameNewBs, str2gErNeopBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gErBulNeop, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    # print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print(f"- Need chack code after table (dfNameNewBs)")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН", "УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)

        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index", "RegUcn", "IO", "IR", 2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df2gErBulNeop, dfDaily, strNoUcn, str2gErBulNeop = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gErBulNeop, dfDaily, "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols2gEr(dfNoUcn)
            if "BS_name_x" in dfNoUcn:
                dfNoUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfNoUcn["TG"] = "0"
            dfNoUcn["SW"] = "-"
            dfNoUcn["RBL2_1"] = "-"
            dfNoUcn["RBL2_2"] = "-"
            dfNoUcn["OETM_1"] = "-"
            dfNoUcn["OETM_2"] = "-"
            if ("BscUcn" in dfNoUcn) and ("LacUcn" in dfNoUcn):
                dfNoUcn.insert(1, "BSC", dfUcn["BscUcn"])
                dfNoUcn.insert(1, "LAC", dfUcn["LacUcn"])
            dfNoUcn = dfNoUcn.reindex(columns=
                ["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2","Sector"]
            )
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df2gErBulNeop, dfUcnTemplate, strUcn1, strUcn2, str2gErBulNeop, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gErBulNeop, dfUcnTemplate,"index", "RegUcn", "BS_name", "RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            # dfUcn = funcCorrectCols2gEr(dfUcn)
            if "BS_name_x" in dfUcn:
                dfUcn.insert(1, "BS_name", dfUcn["BS_name_x"])
            dfUcn["TG"] = "0"
            dfUcn["SW"] = "-"
            dfUcn["RBL2_1"] = "-"
            dfUcn["RBL2_2"] = "-"
            dfUcn["OETM_1"] = "-"
            dfUcn["OETM_2"] = "-"
            if ("BscUcn" in dfUcn) and ("LacUcn" in dfNoUcn):
                dfUcn.insert(1, "BSC", dfUcn["BscUcn"])
                dfUcn.insert(1, "LAC", dfUcn["LacUcn"])
            dfUcn = dfUcn.reindex(columns=
                ["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1","OETM_2", "Sector"]
            )
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    #print(f"+ Correct table dfNew:\n{dfNew}")

    #dfOld = funcCorrectCols2gEr(dfOld)
    if "BS_name_x" in dfOld:
        dfOld.insert(1, "BS_name", dfOld["BS_name_x"])
    dfOld["TG"] = "0"
    dfOld["SW"] = "-"
    dfOld["RBL2_1"] = "-"
    dfOld["RBL2_2"] = "-"
    dfOld["OETM_1"] = "-"
    dfOld["OETM_2"] = "-"
    if ("BscUcn" in dfOld) and ("LacUcn" in dfOld):
        dfOld.insert(1, "BSC", dfUcn["BscUcn"])
        dfOld.insert(1, "LAC", dfUcn["LacUcn"])
    dfOld = dfOld.reindex(columns=["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2","Sector"])
    #print(f"+ Correct table (dfOld):\n{dfOld}")

    df2gErBulNeop, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df2gErBulNeop)\n{df2gErBulNeop}")
    df2gErBulNeop.to_csv("df2gErBulNeop.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    # print(listFiles)
    #for file in listFiles:
    #    if "df2gErBulNeop." in file:
    #        # print(file)
    #        dataFromSite = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path=CONFIG_DATA.get("LINKPO2"),
    #            url=CONFIG_DATA.get("LINKSITE3"),
    #            action_func=funcParsingCes,
    #            filterObjectSite=CONFIG_DATA.get("TEGSSITE6")
    #        )
    #        # print(dataFromSite)
    #        print("+ Add Data (df2gErBulNeop) to site CES")'''
if checkTable(df3gEr) == False:
    print(f"+ Add Empty table (df3gEr):\n{df3gEr}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(), strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY16")
    )
    #print(dfDaily)
    dfOld = pd.merge(df3gEr, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #dfOld = pd.merge(df3gEr, dfDaily, left_on="BS_name", right_on="Namefor3g", how="inner")
    print("- Внимание! необходимо проверить соединение таблиц по стоблцу BS_name. Если таблица находим данные по столбцу Namefor3g, тогда необходимо раскомментировать ниже строки #dfOld = ... и #listTechOld = с заменой на текущие строки в коде и доработать ниже код, особенно с BS_name, Так как столбцы по названию могут отличаться.")
    #print(dfOld)

    dfNameNewBs, df3gEr, dfOld, listNameNewBs, str3gErCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df3gEr, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #dfNameNewBs, df3gEr, dfOld, listNameNewBs, str3gErCol, strOldCol = funcGet1DfFrom2Lists(pd.DataFrame(), df3gEr, dfOld, listNameNewBs, "BS_name", "Namefor3g")
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН","УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        #print(listData)
        #print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        #print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index","RegUcn", "IO", "IR",2
        )
        #print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        #print(dfCoords)
        #dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="Namefor3g", right_on="BS_name", how="inner")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df3gEr, dfDaily, strNoUcn, str3gEr = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df3gEr, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            # print(f"+ Correct table (dfNoUcn):\n{dfNoUcn.to_string()}")
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols3gEr(dfNoUcn)
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "site", "RNC_ID", "URA", "LAC", "RAC", "RRU", "Sector"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("Внимание! необходимо проверить заполнение данных таблицы dfUcn.")
            dfUcn, df3gEr, dfUcnTemplate, strUcn1, strUcn2, str3gEr, strUcnTemplate = funcJoin2Df2(
                dfUcn, df3gEr, dfUcnTemplate,"index","RegUcn","BS_name","RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            #dfUcn = funcCorrectCols3gEr(dfUcn)
            dfUcn = dfUcn.reindex(columns=["Reg", "site", "RNC_ID", "URA", "LAC", "RAC", "RRU", "Sector"])
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    print("- Need add code for correct different LAC/RAC/URA")
    #dfOld = funcCorrectCols3gEr(dfOld)
    dfOld = dfOld.reindex(columns=["Reg", "site", "RNC_ID", "URA", "LAC", "RAC", "RRU", "Sector"])
    #print(dfOld)

    df3gEr, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df3gEr):\n{df3gEr}")
    df3gEr.to_csv("df3gEr.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    # print(listFiles)
    #for file in listFiles:
    #    if "df3gEr." in file:
    #        #print(file)
    #        dataFromSite = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path=CONFIG_DATA.get("LINKPO2"),
    #            url=CONFIG_DATA.get("LINKSITE3"),
    #            action_func=funcParsingCes,
    #            filterObjectSite=CONFIG_DATA.get("TEGSSITE5")
    #        )
    #        # print(dataFromSite)
    #        print("+ Add Data (df3gEr) to site CES")
if checkTable(df4gEr) == False:
    print(f"+ Add Empty table (df4gEr):\n{df4gEr}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY17")
    )
    #print(dfDaily)
    dfOld = pd.merge(df4gEr, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df4gEr, dfOld, listNameNewBs, str4gErCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gEr, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("- Need check code after table (dfNameNewBs) ")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                #print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН","УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df4gEr, dfDaily, strNoUcn, str4gEr = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gEr, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            #dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df4gEr, dfUcnTemplate, strUcn1, strUcn2, str4gEr, strUcnTemplate = funcJoin2Df2(
                dfUcn, df4gEr, dfUcnTemplate,"index","RegUcn","BS_name","RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            dfUcn = dfUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    #print(f"+ Correct table dfNew:\n{dfNew.to_string()}")

    if checkTable(dfNew) == False:
        dfNew["BS_name"] = dfNew["site"].str[:6]
        dfCheckLac = dfNew.groupby("BS_name")["LAC"].transform("nunique")  # Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfNew[~(dfCheckLac >= 2)]  # Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfNew[dfCheckLac >= 2]  # Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.reindex(columns=["BS_name_x", "BS_name_y"])
        dfNewAndNeighbourBS = dfNewAndNeighbourBS.drop_duplicates()
        dfUnCorrect["BS_name"] = dfUnCorrect["BS_name"].astype(str)  # добавил из-за ошибки: ValueError: You are trying to merge on object and float64 columns for key 'BS_name'. If you wish to proceed you should use pd.concat
        dfNewAndNeighbourBS["BS_name_x"] = dfNewAndNeighbourBS["BS_name_x"].astype(str)  # добавил из-за ошибки: ValueError: You are trying to merge on object and float64 columns for key 'BS_name'. If you wish to proceed you should use pd.concat
        print(f"- Need check code for table (dfUnCorrect)")
        dfUnCorrect = pd.merge(dfUnCorrect, dfNewAndNeighbourBS, left_on="BS_name", right_on="BS_name_x", how="inner")
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1  # Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name_y"] + dfUnCorrect["BS_Id"].astype(str)
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        #print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        # print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfUnCorrect = dfUnCorrect.reindex(columns=["Reg", "site", "LAC", "Sector"])
        dfCorrect = dfCorrect.reindex(columns=["Reg", "site", "LAC", "Sector"])
        #print(f"+ Correct tables (dfUnCorrect,dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        dfNew, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        #print(f"+ Correct table (dfNew):\n{dfNew.to_string()}")
    #dfOld = funcCorrectCols4gEr(dfOld)
    if checkTable(dfOld) == False:
        dfOld = dfOld.reindex(columns=["Reg", "site", "LAC", "Sector"])
        #print(f"+ Correct table dfOld:\n{dfOld.to_string()}")
        #dfCheckLac = dfOld
        dfOld["BS_name"] = dfOld["site"].str[:6]
        #print(f"+ Correct table dfOld:\n{dfOld}")
        dfCheckLac = dfOld.groupby("BS_name")["LAC"].transform("nunique")  # Считаем количество УНИКАЛЬНЫХ LAC для каждой BS_name
        dfCorrect = dfOld[~(dfCheckLac >= 2)]  # Удаляем строки, у которых 2 и более LAC (оставляем те, у которых МЕНЬШЕ 2)
        dfUnCorrect = dfOld[dfCheckLac >= 2]  # Фильтруем исходный DataFrame (оставляем только те, где уникальных LAC >= 2)
        #print(f"+ Add tables (dfUnCorrect, dfCorrect):\n{dfUnCorrect}\n{dfCorrect}")
        print(f"- Need check code for table (dfUnCorrect)")
        dfCheckSector = dfUnCorrect["Sector"].str[-1].astype(int)
        dfUnCorrect["BS_Id"] = ((dfCheckSector - 1) % 3) + 1  # Применяем формулу циклического сдвига (каждые 3 шага результат повторяется)
        dfUnCorrect["CellId"] = dfUnCorrect["BS_name"] + dfUnCorrect["BS_Id"].astype(str)
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY15")
        )
        #print(f"+ Add table (dfDaily):\n{dfDaily}")
        dfUnCorrect = pd.merge(dfUnCorrect, dfDaily, left_on="CellId", right_on="CellId", how="inner")
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        if "LAC_y" in dfUnCorrect:
            dfUnCorrect.insert(1, "LAC", dfUnCorrect["LAC_y"])
        dfUnCorrect = dfUnCorrect.reindex(columns=["Reg", "site", "LAC", "Sector"])
        dfUnCorrect = dfUnCorrect.drop_duplicates()
        dfCorrect = dfCorrect.reindex(columns=["Reg", "site", "LAC", "Sector"])
        #print(f"+ Correct table (dfUnCorrect):\n{dfUnCorrect}")
        #print(f"+ Correct table (dfCorrect):\n{dfCorrect}")
        dfOld, dfUnCorrect, dfCorrect = funcJoin2Df(pd.DataFrame(), dfUnCorrect, dfCorrect)
        #print(f"+ Correct table (dfOld):\n{dfOld}")

    df4gEr, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df4gEr):\n{df4gEr.to_string()}")
    df4gEr.to_csv("df4gEr.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    # print(listFiles)
    #for file in listFiles:
    #    if "df4gEr." in file:
    #        #print(file)
    #        dataFromSite = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path=CONFIG_DATA.get("LINKPO2"),
    #            url=CONFIG_DATA.get("LINKSITE3"),
    #            action_func=funcParsingCes,
    #            filterObjectSite=CONFIG_DATA.get("TEGSSITE4")
    #        )
    #        # print(dataFromSite)
    #        print("+ Import file (df4gNok) to site CES")
if checkTable(df4gErBul) == False:
    print(f"+ Add Empty table (df4gErBul):\n{df4gErBul}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(),strAcesNokia,strUces,strPces,"Config_all", CONFIG_DATA.get("DBQUERRY17")
    )
    #print(dfDaily)
    dfOld = pd.merge(df4gErBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(f"+ Add table dfOld:\n{dfOld.to_string()}")

    dfNameNewBs, df4gErBul, dfOld, listNameNewBs, str4gErBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gErBul, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print(f"- Need check code after table (dfNameNewBs)")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData, "УЦН","УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        #dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        #print(f"+ Add table (dfUcnTemplate):\n{dfUcnTemplate}")

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df4gErBul, dfDaily, strNoUcn, str4gErBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gErBul, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            # print(dfUcn)
            dfUcn, df4gErBul, dfUcnTemplate, strUcn1, strUcn2, str4gErBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df4gErBul, dfUcnTemplate,"index","RegUcn","BS_name","RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            dfUcn = dfUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            #dfUcn = funcCorrectCols4gEr(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    #print(f"+ Correct table (dfNew):\n{dfNew}")

    #dfOld = funcCorrectCols4gEr(dfOld)
    dfOld = dfOld.reindex(columns=["Reg", "site", "LAC", "Sector"])
    #print(f"+ Correct table (dfOld):\n{dfOld}")

    df4gErBul, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df4gErBul):\n{df4gErBul}")
    df4gErBul.to_csv("df4gErBul.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    # print(listFiles)
    #for file in listFiles:
    #    if "df4gErBul." in file:
    #        #print(file)
    #        dataFromSite = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path=CONFIG_DATA.get("LINKPO2"),
    #            url=CONFIG_DATA.get("LINKSITE3"),
    #            action_func=funcParsingCes,
    #            filterObjectSite=CONFIG_DATA.get("TEGSSITE4")
    #        )
    #        # print(dataFromSite)
    #        print("+ Add Data (df4gErBul) to site CES")
if checkTable(df4gErBulNeop) == False:
    print(f"+ Add Empty table (df4gErBulNeop):\n{df4gErBulNeop}")
    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
        pd.DataFrame(), strAcesNokia,strUces,strPces, "Config_all", CONFIG_DATA.get("DBQUERRY17")
    )
    #print(dfDaily)
    dfOld = pd.merge(df4gErBulNeop, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(f"+ Add table dfOld:\n{dfOld.to_string()}")

    dfNameNewBs, df4gErBulNeop, dfOld, listNameNewBs, str4gErBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gErBulNeop, dfOld, listNameNewBs,"BS_name", "BS_name"
    )
    #print(dfNameNewBs)
    dfNew = pd.DataFrame()
    dfNewAndNeighbourBS = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print(f"- Need check code after table (dfNameNewBs)")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")
                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingBars,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)
                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,"УЦН","УЦН", "-"
                )
                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,"index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbQuerry = funcImportSqlToPandas2(
            pd.DataFrame(),strAcesNokia,strUces,strPces,"Physical_param", CONFIG_DATA.get("DBQUERRY14")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        #dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        #print(f"+ Add table (dfUcnTemplate):\n{dfUcnTemplate}")

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df4gErBulNeop, dfDaily, strNoUcn, str4gErBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gErBulNeop, dfDaily,"index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            dfNewAndNeighbourBS = dfNoUcn
            print(f"+ Add table (dfNewAndNeighbourBS):\n{dfNewAndNeighbourBS.to_string()}")
            #dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            # print(dfUcn)
            dfUcn, df4gErBulNeop, dfUcnTemplate, strUcn1, strUcn2, str4gErBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df4gErBulNeop, dfUcnTemplate, "index","RegUcn","BS_name","RegUcn"
            )
            print(f"+ Correct table (dfUcn):\n{dfUcn}")
            dfUcn = dfUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            #dfUcn = funcCorrectCols4gEr(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    #print(f"+ Correct table (dfNew):\n{dfNew}")

    # dfOld = funcCorrectCols4gEr(dfOld)
    dfOld = dfOld.reindex(columns=["Reg", "site", "LAC", "Sector"])
    # print(f"+ Correct table (dfOld):\n{dfOld}")

    df4gErBulNeop, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print(f"+ Correct Empty table (df4gErBulNeop):\n{df4gErBulNeop}")
    df4gErBulNeop.to_csv("df4gErBulNeop.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")
    #listFiles = os.listdir()
    # print(listFiles)
    #for file in listFiles:
    #    if "df4gErBulNeop." in file:
    #        #print(file)
    #        dataFromSite = funcPowerDrivaer(
    #            driver_path = '\\\\' + strDnetFolder + '\\' + CONFIG_DATA.get("LINKNETPATH1") + '\\yandexdriver.exe',
    #            binary_path=CONFIG_DATA.get("LINKPO2"),
    #            url=CONFIG_DATA.get("LINKSITE3"),
    #            action_func=funcParsingCes,
    #            filterObjectSite=CONFIG_DATA.get("TEGSSITE4")
    #        )
    #        # print(dataFromSite)
    #        print("+ Add Data (df4gErBulNeop) to site CES")

if (checkTable(df2gNok) == True) and (checkTable(df2gNokBul) == True) and (checkTable(df3gNok) == True) and (checkTable(df4gNok) == True )and (checkTable(df4gNokBul) == True) and (checkTable(df2gEr) == True) and (checkTable(df2gErBul) == True) and (checkTable(df2gErBulNeop) == True) and (checkTable(df3gEr) == True) and (checkTable(df4gEr) == True) and (checkTable(df4gErBul) == True) and (checkTable(df4gErBulNeop) == True):
    print("+ All data on the CES website is filled in.")
