from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def war(username, password, display_name):
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Firefox(options=options)

    driver.set_page_load_timeout(5)

    print(f"Username: {username}")
    print(f"Password: {password}")

    login(driver, username, password, display_name)
    
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit")
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "rinfo")))           
            # Keep this up to date
            # ganti dengan matkul yang namanya pasti ada
            if ("Analisis Numerik" in driver.page_source):
                break
            raise NoSuchElementException
        except:
            print("Retrying... (Belum mulai)")
            logout(driver)
            login(driver, username, password, display_name)
            continue

    matkul=[]
    with open('matkul.txt') as file_inp:
        for line in file_inp:
            matkul.append(line.strip())
        print("Matkul Loaded")

    try:
        for kelas in matkul:
            try:
                radio_input = driver.find_element_by_xpath('//input[@value="{}"]'.format(kelas))

                if(not radio_input.is_selected()):
                    radio_input.click()
                    print(f"{kelas} chosen!)")
                    time.sleep(0.1)
                else:
                    print(f"{kelas} SUDAH DIPILIH!)")
                    time.sleep(30)
            except:
                raise NoSuchElementException
                break
    except NoSuchElementException:
        print("input tidak valid")
        print("EXITING...")
    else:
        driver.find_element_by_name('submit').click()
        while True:
            if ("IRS berhasil tersimpan!" in driver.page_source or "Daftar IRS" in driver.page_source):
                print("Process finished! Press enter to exit...")
                break
            else:
                print("Mencoba simpan IRS...")
                driver.refresh()

    input()
    driver.close()

def login(driver, username, password, display_name):
    print("Logging in...")

    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/")
            element = driver.find_element_by_id("u")
            element.send_keys(username)
            element = driver.find_element_by_name("p")
            element.send_keys(password)
            element.send_keys(Keys.RETURN)
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "rinfo")))     
        except:
            try:
                driver.get("https://academic.ui.ac.id/main/Welcome/")
                if (("Logout Counter" in driver.page_source or display_name in driver.page_source) and "S1 Reguler Ilmu Komputer" in driver.page_source):
                    print("Logged in!")
                    break
                else:
                    print("Role Error")
                    logout(driver)
            except:
                continue

        try:
            if (("Logout Counter" in driver.page_source or display_name in driver.page_source) and "S1 Reguler Ilmu Komputer" in driver.page_source):
                print("Logged in!")
                break
            else:
                print("Role Error")
                logout(driver)
            raise Exception
        except:
            continue
        
def logout(driver):
    print("Logging out...")

    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/Logout")
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "u")))
        except:
            try:
                driver.get("https://academic.ui.ac.id/main/Welcome/")
                driver.find_element_by_id("u")
                print("Logged out!")
                break
            except:
                continue
        
        try:
            driver.find_element_by_id("u")
            print("Logged out!")
            break
        except:
            continue

if __name__ == "__main__":
    print("Starting...")
    uspass=[]
    with open('credentials.txt') as file_inp:
        for line in file_inp:
            uspass.append(line.strip())

    war(uspass[0],uspass[1], uspass[2])