# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:59:15 2022

@author: Kaen

{
    "nombre":"Kevin Acosta",
    "numtel":"59598566482",
    "canal":"",
    "detalle":{
        "":""
    }
}

NIS:2314468




"""
from cmath import e
from flask import Blueprint, request, jsonify
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
from datetime import datetime


import time

# Utilitarios para sistema operativo

import os, signal
from PIL import Image
import requests
import calendar

gmt = time.gmtime()

ruta_img = "/var/www/html/josefina/chrome/"
name_img = ""
timer = time.time()
mainpath = "/var/www/html/josefina/chrome/"

buscarProducto = Blueprint('buscarProducto', __name__)

@buscarProducto.route('/buscarProducto',methods=['POST'])


#Logica

def llamarServicioSet():
    global nombre,telefono,canal,detalle
    #producto =  request.json['producto']
    scrapSeis(request)
    #if canal == 'ANDE':
        #scrapAnde(request)
    #elif canal == 'CLARO':
        #scrapClaro(request)
 
    salida = {'codRes': codRes, 'menRes' : menRes, 'datos' : resPath}
    return jsonify({'ParmOut': salida})







"""
*******BUSCAR PRODUCTO********
"""

def scrapSeis(request):
    global fullpath,options,driver_path,driver,PID
    global nombre,telefono,canal,detalle
    global codRes, menRes, resPath
    
    try:
        
        producto = request.json['producto']
        print('Producto a buscar--->', producto)

        #fullpath = os.path.join(mainpath)
        
        # Opciones de Navegacion
       
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        print("Despues de opciones")
        driver = webdriver.Chrome(chrome_options=options, executable_path=r'/opt/bonus/chromedriver')
        print("Driver")
        #Driver para Windows
        #driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\\chrome\\chromedriver.exe')
        print(driver)
        PID = driver.service.process.pid ##ID proceso Chromedriver
        print('PID: ' + str(PID))
        ##driver.implicitly_wait(10)
        driver.set_page_load_timeout(25)

        #Inicializamos el Navegador 
        driver.get('https://www.superseis.com.py/search.aspx?searchterms='+producto)
        print("Get")
        #driver.get('https://www.superseis.com.py/AddToCart.aspx?ProductId=259846&Cantidad=1&Container=Modulo%20de%20Busquedas&ButtonParameters=Pagina%20principal')
        time.sleep(2)
        
        print('ELEMENTOS1 -->')
        
        
        pagination = driver.find_elements(By.XPATH,"//div[@class='product-pager']/div/div/a[contains(@href,'https://www.superseis.com.py/search.aspx?searchterms=')]")
        textP = []
        last = 0
        
        for j in range(len(pagination)):
            if pagination[j].text == 'Último':
                last = 1
                href = pagination[j].get_attribute("href")
                index = href.index('&') + 11
                print('link',index)
                penultima = href[index::]
                print('numero',penultima)
                
            else:
                textP.append(pagination[j].text)
                #print('link',pagination[i].get_attribute("href"))
         
        
        if last == 0:
            penultima = pagination[textP.index('Siguiente')-1].get_attribute("href")[-1]
        
        print('Titulo-->',penultima)
        lista = []
        convertint = int(penultima)
        print(type(convertint))
        
        
        
        for count in range(convertint):
            #print('entre')
            time.sleep(3)
            
            elements = driver.find_elements(By.XPATH,"//div[@class='item-box']/div")
            #print('entre1')
            precio = driver.find_elements(By.XPATH,"//div[@class='prices']/*[@class='productPrice']/*[@class='price-label']")
            #print('entre2')
            titulo = driver.find_elements(By.XPATH,"//*[@class='product-title']/*[@class='product-title-link']")
            #print('entre3')
            #print('ELEMENTOS1.2 -->',pagination)
        
            #print('ELEMENTOS1.2 -->',len(elements))
        
            #print('PRECIO-->',precio)
        
        
        
            
        
            for i in range(len(elements)):
                #print('PRECIO-->',precio[i].text)
                print('Titulo-->',titulo[i].text)
                #print('ClassName -->',elements[i].get_attribute("class")[20:-1])
                valorlista = {"precio":precio[i].text,"nombre":titulo[i].text,"codProducto":elements[i].get_attribute("class")[20::]}
                lista.append(valorlista)
                #print('Lista -->',lista)
        
        
            print('entre4')
            elementS = driver.find_elements(By.XPATH,"//div[@class='product-pager']/div/div/a[contains(text(),'Siguiente')]")
            
            if len(elementS) > 0:
                print('HAY')
                siguiente = driver.find_element(By.XPATH,"//div[@class='product-pager']/div/div/a[contains(text(),'Siguiente')]")
                siguiente.click()
            else:
                print('OPA')
            time.sleep(3)
            #print('Lista-->>', len(lista))
        print('Lista-->>', len(lista))
        driver.close()
        driver.quit()
            
            
    
        codRes = 'SIN_ERROR'
        menRes = 'OK'
        resPath = lista
    except Exception as e:
        codRes = 'ERROR'
        menRes = e
        resPath = 'NULL'
    
    
    
    
    
    
    
    
    
    
    





