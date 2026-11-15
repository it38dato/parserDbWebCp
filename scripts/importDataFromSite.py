from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time

def funcPowerDrivaer(driver_path, binary_path, url, action_func, filterObjectSite):
    op = Options()
    op.add_argument("--headless=new")
    op.add_argument("--window-size=1920,1080")
    op.binary_location = binary_path
    service = Service(executable_path=driver_path)
    #browser = webdriver.Chrome(service=service)
    browser = webdriver.Chrome(service=service, options=op)
    #print("+ Set parameters browser")
    try:
        browser.get(url)
        result = action_func(browser, filterObjectSite)
        #print(f"+ Add object (result)")
        return result
    except Exception as e:
        # СОХРАНЯЕМ СКРИНШОТ ПРИ ЛЮБОЙ ОШИБКЕ
        browser.save_screenshot("error_debug.png")
        print(f"- Error. The screenshot has been saved as error_debug.png.: {e}")
        raise e # Пробрасываем ошибку дальше, чтобы видеть Traceback
    finally:
        browser.quit()
def funcFindAndClickObjectSite(browser, tegSearch, tegClick, filter):
    findSearch = browser.find_element(By.NAME, tegSearch)
    findSearch.send_keys(filter + "\n")
    #print("+ Add str object (findSearch) for search button in browser")
    findClick = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, tegClick))
    )
    findClick.click()
    #print("+ Click str object (findClick)")
    return browser, tegSearch, tegClick, filter
def funcFindObjectsSite(browser, teg, listTeg):
    listTeg = browser.find_elements(By.CSS_SELECTOR, teg)
    #print(f"+ Add list (listTeg):\n {listTeg}")
    return browser, teg, listTeg
def funcFindFilterClick2ObjectSite(browser, tegSearch1, tegSearch2, tegClick, filter1, filter2):
    findSearch1 = browser.find_element(By.ID, tegSearch1)
    findSearch2 = browser.find_element(By.ID, tegSearch2)
    findSearch1.send_keys(filter1)    
    findSearch2.send_keys(filter2)
    # print("+ Add str objects (findSearch1, findSearch2) for search button in browser")
    findClick = browser.find_element(By.CSS_SELECTOR, tegClick)
    findClick.click()
    # print("+ Click str object (findClick)")
    return browser, tegSearch1, tegSearch2, tegClick, filter1, filter2
def funcFindFilterClick1ObjectSite(browser, tegSearch, tegClick, filter):
    findSearch = browser.find_element(By.XPATH, tegSearch)
    findSearch.send_keys(filter)
    # print("+ Add str object (findSearch) for search button in browser")
    findClick = browser.find_element(By.CSS_SELECTOR, tegClick)
    findClick.click()
    # print("+ Click str object (findClick)")
    return browser, tegSearch, tegClick, filter
def funcClick1ObjectSite(browser, tegClick):
    findClick = browser.find_element(By.CSS_SELECTOR, tegClick)
    findClick.click()
    # print("+ Click str object (findClick)")
    return browser, tegClick
def funcClickAlert1ObjectSite(browser, tegClick):
    findClick = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, tegClick))
    )
    browser.execute_script("arguments[0].click();", findClick)
    try:
        WebDriverWait(browser, 5).until(EC.alert_is_present())
        alert = browser.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("- Alert did not appear, continuing.")
    return browser, tegClick
def funcFindObjectSite(browser, tegSearch, findSearch):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    findSearch = soup.find_all(class_=tegSearch)
    # print("+ Click str object (findSearch)")
    return browser, tegSearch, findSearch
# Функция закрывает модальные окна веб сайта:
def funcCloseWindow(browser, teg):
    try:
        findBtnClose = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, teg)))
        print(f"+ Add str object (findBtnClose)")
        findBtnClose.click()
        print(f"+ Click str object (findBtnClose) (close/закрыть)")
        print("- Need check. Скрипт не сразу находит нужный объект и почему то находит Амур и 25 БС, проблема с ожиданием. необохимдо проверить.")
        time.sleep(10)
        print("- Need check. Скрипт не сразу находит нужный объект и почему то находит Амур и 25 БС, проблема с ожиданием. необохимдо проверить.")
    except Exception:
        print("- The modal window did not appear or could not be closed")
    return browser, teg
# Функция ищет поиск и находит объект:
def funcSearchBrowser(browser, teg, filter):
    findSearch = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, teg))
    )
    #print("+ Add search field on the page")
    findSearch.click()
    findSearch.clear()
    #print("+ Click str object (findSearch)")
    findSearch.send_keys(filter)
    findSearch.send_keys(Keys.ENTER)
    #print("+ Add str object (findSearch) for search button in browser")
    time.sleep(5)
    return browser, teg, filter
# Функция которая ищет таблицу, находит ссылку и нажимает на нее. разница функций в фильтрации объекта:
def funcFindTableClick(browser, tegTbody, tegTr, tegTdA):
    findTable = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, tegTbody))
    )
    print(f"+ Find object (findTable)")
    findRows = findTable.find_elements(By.XPATH, tegTr)# Каждая строка — это тег tr с атрибутом data-index
    countRows = len(findRows)
    print(f"+ Add int object (countRows) count rows in table: {countRows}")
    if countRows > 1:# Если строк больше одной — ничего не нажимаем, просто пишем сообщение
        print("- The press has been cancelled. Two objects (or more) were found. It may be necessary to restart the script.")
    elif countRows == 1:# Если строка ровно одна, работаем с ней
        findRow = findRows[0]
        try:
            findClick = findRow.find_element(By.XPATH, tegTdA)
            #print(f"+ Find object (findClick)")
            findNameClick = findClick.text
            #print(f"+ Read object (findClick)")
            findClick.click()
            print(f"+ Move to the str object (findNameClick): {findNameClick}!")
        except Exception as e:
            print(f"- Error. The link could not be found or clicked (Наименование):\n{e}")
    else:
        print("- The table is empty, no objects found")
    time.sleep(5)
    return browser, tegTbody, tegTr, tegTdA
# Функция которая ищет таблицу, находит ссылку и нажимает на нее. разница функций в фильтрации объекта. здесь фильтр стоит на объект и дробь:
def funcFindTableClick2(browser, tegTbody, tegTr, tegTdA):
    findTable = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, tegTbody))
    )
    findRows = findTable.find_elements(By.XPATH, tegTr)
    countRows = len(findRows)
    print(f"+ Add int object (countRows) count rows in table: {countRows}")
    if countRows > 0:
        numbMax = -1
        findClick = None
        findNameClick = ""
        for row in findRows:
            try:
                findA = row.find_element(By.XPATH, tegTdA)
                findNameA = findA.text.strip()
                #print(f"+ Add object (findNameA) for search teg (a) acandidate")
                match = re.search(r'/(\d+)$', findNameA)
                #print(f"+ Add object (match) for search number after symbol /")
                if match:
                    numbCut = int(match.group(1))
                    #print(f"+ Add int object (numbCut) for search number after symbol /")
                else:
                    numbCut = 0
                    #print(f"+ Add int object (numbCut) for search number after symbol /")
                if numbCut > numbMax:
                    numbMax = numbCut
                    findClick = findA
                    findNameClick = findNameA
                    #print(f"+ Chek object (numbCut) for search latest (numbMax) candidate")
            except Exception:
                continue# Пропускаем служебные или пустые строки, если они попадутся
        if findClick:
            print(f"+ Add str object (findNameClick) latest candidate: {findNameClick}")
            findClick.click()
            print(f"+ Click str object (findNameClick): {findNameClick}!")
        else:
            print("- Error. It was not possible to extract the candidates numbers from the table.")
    else:
        print("- The table is empty, no objects found")
    time.sleep(5)
    return browser, tegTbody, tegTr, tegTdA
# Функция ищет меню по тегам div:
def funcFimdMenuClick(browser, tegDivClick, tegDivInput):
    try:
        findDiv = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, tegDivClick))
        )
        #print(f"+ Add onject (findDiv) for search teg (tegDivClick): {tegDivClick}")
        findDiv.click()
        print(f"+ Click menu (Общая информация) teg data-tab-name!")
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, tegDivInput))
        )
        #print(f"+ Waiting for content to load")
    except Exception as e:
        print(f"- Error after Click menu (Общая информация):\n{e}")
    time.sleep(5)
    return browser, tegDivClick, tegDivInput
# Функцию ищет форму и выводит список необходимой информации по значению (Value), которое необохимдо выывести. Value, input теги должны соотсветствовать:
def funcFindFornmFilterInputValue(browser, tegForm, tegInputDiv, listInputs):
    findForm = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, tegForm))
    )
    #print(f"+ Add object (findForm) using teg: {tegForm}")
    findInput = findForm.find_elements(
        By.XPATH, tegInputDiv
    )
    #print(f"+ Add object (findInput) for search all elements using teg: {tegInputDiv}")
    for i in findInput:
        findTeg = i.tag_name
        # print(f"+ Add object (findTeg) using teg: {tag_name}")
        if findTeg == "input":
            findValue = i.get_attribute("value")
            # print(f"+ Add object (findValue) using teg: {value}")
        else:
            findValue = i.text.strip()
            # print(f"+ Add object (findValue) using text")
        listInputs.append(findValue)
    #print(f"+ Add list (listInputs):\n {listInputs}")
    return  browser, tegForm, tegInputDiv, listInputs
