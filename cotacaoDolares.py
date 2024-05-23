from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import os
import json
import time
import random

def get_webDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('headless')

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
        driver.get("https://www.google.com/search?q=" + dolar + "+hoje+cotação")
        time.sleep(1)
        valor = driver.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')
        modificador = random.randint(-5, 5)
        val = float(valor.text.replace(",", "."))
        if val>=1:
            val += modificador/100
        elif val<1 and val>=0.1:
            val += modificador/1000
        elif val<0.1 and val>=0.01:
            val += modificador/10000
        if dolar == "D\u00f3lar Liberiano":
            print(f'{val:.4f}')
            print(f'{round(val, 4):.4f}'.replace(".", ","))
        valores[data].append({dolar: f'{round(val, 4):.4f}'.replace(".", ",")})
        # valores[data].append({dolar: valor.text})
    driver.close()
    driver.quit()
    if os.path.exists("valores_dolares.json"):
        with open("valores_dolares.json", "r") as val:
            dump = json.load(val)
        with open("valores_dolares.json", "w") as dump_f:
            dump[data] = valores[data]
            json.dump(dump, dump_f)
    else: 
        with open("valores_dolares.json", "w") as f:
            json.dump(valores, f)
    

if __name__ == "__main__":
        getDolarValues()