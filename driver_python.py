from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import sqlite3

option = webdriver.ChromeOptions()
option.add_argument("--headless")
option.add_argument("hide_console")
driver = webdriver.Chrome(executable_path="chromedriver Path", options=option)
driver.get("https://www.tgju.org/profile/geram18/history")
connection = sqlite3.connect("project.db Path")
c = connection.cursor()
c.execute("PRAGMA table_info(driver)")
data = (c.fetchall())

if len(data[0][1]) != 1:
        for i in range(0, 8):
                c.execute(f'''ALTER TABLE driver RENAME COLUMN '{data[i][1]}'  TO "{i + 1}"''')

def site(driver):
        li = []
        class_list_low = []
        class_list_high = []
        for k in range(1, 31):
                li.append([0, 0, 0, 0, 0, 0, 0, 0])

        content1 = driver.find_elements_by_class_name('low')
        for i in range(0, len(content1)):
                txt = content1[i].text
                if ')' not in txt:
                        class_list_low.append(txt)
        time.sleep(5)
        content2 = driver.find_elements_by_class_name('high')
        for i in range(0, len(content2)):
                txt = content2[i].text
                if ')' not in txt:
                        class_list_high.append(txt)
        time.sleep(5)

        for k in range(1, 31):  # 31
                for i in range(1, 5):
                        path_main = f"/html/body/main/div[1]/div[2]/div/div[1]/div/div[3]/div/table/tbody/tr[{k}]/td[{i}]"
                        element = driver.find_element_by_xpath(path_main)
                        li[k - 1][i - 1] = element.text
                for i in range(5, 7):
                        path_main = f"/html/body/main/div[1]/div[2]/div/div[1]/div/div[3]/div/table/tbody/tr[{k}]/td[{i}]/span"
                        try:
                                element = driver.find_element_by_xpath(path_main)
                                if element.text in class_list_low:
                                        li[k - 1][i - 1] = "-" + element.text

                                if element.text in class_list_high:
                                        li[k - 1][i - 1] = "+" + element.text
                        except:
                                li[k - 1][i - 1] = ""

                for i in range(7, 9):
                        path_main = f"/html/body/main/div[1]/div[2]/div/div[1]/div/div[3]/div/table/tbody/tr[{k}]/td[{i}]"
                        element = driver.find_element_by_xpath(path_main)
                        li[k - 1][i - 1] = element.text
                if k % 3 == 0:
                        element = driver.find_element_by_xpath(
                                f"/html/body/main/div[1]/div[2]/div/div[1]/div/div[3]/div/table/tbody/tr[{k}]/td[1]")
                        driver.execute_script('arguments[0].scrollIntoView(true);', element)
                        time.sleep(5)
        return li


def scroll_click(driver):
        element = driver.find_element_by_xpath(
                "/html/body/main/div[1]/div[2]/div/div[1]/div/div[3]/div/table/tbody/tr[25]/td[1]")
        driver.execute_script('arguments[0].scrollIntoView(true);', element)
        element = driver.find_element_by_xpath('//*[@id="DataTables_Table_0_next"]')
        print(element)
        ActionChains(driver).move_to_element(element).click().perform()
        time.sleep(5)


def save(var):
        connection = sqlite3.connect("project.db Path")
        c = connection.cursor()

        for i in range(0, len(var)):
                sqlite_insert_query = f"""INSERT INTO driver
                                  ('1','2','3','4','5','6','7','8')
                                   VALUES
                                   ('{var[i][0]}','{var[i][1]}','{var[i][2]}','{var[i][3]}','{var[i][4]}','{var[i][5]}',
                                   '{var[i][6]}','{var[i][7]}')"""

                c.execute(sqlite_insert_query)

        connection.commit()
        connection.close()

for i in range(1, 85):
        var = site(driver)
        scroll_click(driver)
        save(var)


connection = sqlite3.connect("project.db Path")
c = connection.cursor()

c.execute(f'''ALTER TABLE driver RENAME COLUMN '1'  TO بازگشايي''')
c.execute(f'''ALTER TABLE driver RENAME COLUMN '2'  TO کمترين''')
c.execute(f'''ALTER TABLE driver RENAME COLUMN '3'  TO بيشترين''')
c.execute(f'''ALTER TABLE driver RENAME COLUMN '4'  TO پاياني''')
c.execute(f'''ALTER TABLE driver RENAME COLUMN '5'  TO "ميزان تغيير"''')
c.execute(f'''ALTER TABLE driver RENAME COLUMN '6'  TO "درصد تغيير"''')
c.execute(f'''ALTER TABLE driver RENAME COLUMN '7'  TO "تاريخ/ميلادي"''')
c.execute(f'''ALTER TABLE driver RENAME COLUMN '8'  TO "تاريخ/شمسي" ''')
connection.close()
