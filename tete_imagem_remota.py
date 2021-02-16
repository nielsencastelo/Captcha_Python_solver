# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:40:05 2020

@author: Nielsen
"""

import base64
from google.cloud import vision
import os
import io
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="G:/NCDD/API_Project-af72e383d721.json"
#print(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) 

client = vision.ImageAnnotatorClient()
image = vision.types.Image()

url = 'https://iptu.prefeitura.sp.gov.br/'
options = Options()
#options.add_argument('--headless')
#options.add_argument('--window-size=1920,1080')
#options.add_argument('--user-agent=5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')

driver = webdriver.Chrome(chrome_options=options)


#driver = webdriver.Firefox()

driver.maximize_window()

driver.get(url)
driver.implicitly_wait(100)

WAIT = True

while WAIT:
    try:
        driver.find_element_by_tag_name('body')

        WAIT = False
    except:
        pass
        


time.sleep(1)
url_atr = driver.find_element_by_id('captchaImagem').get_attribute('src')

time.sleep(2)

imagem = url_atr[23:]

with open(r"image.jpg", 'wb') as f:
    f.write(base64.b64decode(imagem))
        
file_name = os.path.abspath('image.jpg')

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.text_detection(image=image)
texts = response.text_annotations

text = texts[0]
captchar_result = text.description.replace('\n','')
print('Captchar: ',captchar_result)

tempo = 3

numero_contribuinte = '1201980031-3'
time.sleep(tempo)
driver.find_element_by_id('txtNumeroContribuinte').clear()

for i in list(numero_contribuinte):
    time.sleep(0.2)
    driver.find_element_by_id('txtNumeroContribuinte').send_keys(i)

time.sleep(tempo)

# seleciona a parcela a vista
select = Select(driver.find_element_by_id('comboBoxParcela'))
select.select_by_index(10)


time.sleep(tempo)
driver.find_element_by_id('txtExercicio').clear()
exercicio = '2020'
for i in list(exercicio):
    time.sleep(0.2)
    driver.find_element_by_id('txtExercicio').send_keys(i)
    
time.sleep(tempo)
driver.find_element_by_id('txtCaptcha').clear()

for i in list(captchar_result):
    time.sleep(0.2)
    driver.find_element_by_id('txtCaptcha').send_keys(i)

time.sleep(tempo)
#driver.find_element_by_id('btnGerarSegundaVia').click()
driver.find_element_by_id('txtCaptcha').send_keys(Keys.ENTER)

try:
    alert = driver.find_element_by_id('divMensagem')
    print('Mensagem: ',alert.text)
except:
    valor = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td[1]/table[1]/tbody/tr[12]/td[2]/table/tbody/tr[2]/td/label/b')
    print('Valor: ',valor.text)
    driver.back()




#driver.quit()


