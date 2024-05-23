from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import os
import json
import time

def get_webDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option("detach", True)

    return webdriver.Chrome(options=options)

def dumpDolarNames():
    driver = get_webDriver()
    driver.get("https://www.google.com/search?q=todos+os+dolares+atuais")
    time.sleep(2)
    select = driver.find_element(By.CLASS_NAME, "zuzy3c")
    options = [op.text for op in select.find_elements(By.TAG_NAME, "option") if "Dólar" in op.text]
    with open("dump_nome_dolares.json", "w") as f:
        json.dump(options, f)
    driver.close()
    driver.quit()

def getDolarValues():
    driver = get_webDriver()
    data = date.today().strftime("%Y-%m-%d")
    valores = {data: []}
    with open("dump_nome_dolares.json", "r") as f:
        dolares = json.load(f)
    for dolar in dolares:
        driver.get("https://www.google.com/search?q=" + dolar + "+hoje")
        time.sleep(1)
        valor = driver.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')
        valores[data].append({dolar: valor.text})
    driver.close()
    driver.quit()
    if os.path.exists("valores_dolares.json"):
        with open("valores_dolares.json", "r") as f:
            valores.update(json.load(f))
    else: 
        with open("valores_dolares.json", "w") as f:
            json.dump(valores, f)
    

if __name__ == "__main__":
    getDolarValues()