import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from mysql.connector import Error
from mysql.connector import Error
from PF_ArchivoConstantes_CS import data_csv, data_limpieza
from S2_Limpieza_CS import LimpiadorCSV
from S3_Conexion_CS import DataBaseProyecto

def iniciar_navegador():
    s = Service(ChromeDriverManager().install())
    opc = Options()
    opc.add_argument("--window-size=1020,1200")

    navegador = webdriver.Chrome(service=s, options=opc)
    return navegador

def cerrar_navegador(navegador):
    navegador.quit()

def cargar_pagina(navegador, url):
    navegador.get(url)
    time.sleep(10)

def hacer_clic(navegador, by, value):
    elemento = navegador.find_element(by, value=value)
    elemento.click()
    time.sleep(5)

def obtener_datos_producto(div):
    productname = div.find("h3", attrs={"class": "product-name"})
    actualprice = div.find("p", attrs={"class": "sale-price-product"})
    oldprice = div.find("p", attrs={"class": "price-product"})
    payment = div.find("div", attrs={"class": "meses-telmex"})
    return {
        "Producto": productname.text if productname else "NA",
        "Precio Actual": actualprice.text if actualprice else 0,
        "Precio Anterior": oldprice.text if oldprice else 0,
        "Forma de pago": payment.text if payment else "NA",
    }
def filtrado(navegador, filtro):
    dt = {"Clasificacion": [], "Producto": [], "Precio Actual": [], "Precio Anterior": [], "Forma de pago": []}

    for filtro_id in filtro:
        hacer_clic(navegador, By.ID, filtro_id)

        soup = BeautifulSoup(navegador.page_source, "html.parser")
        lista_divs = soup.find_all(name="div", attrs={"class": "tarjeta-producto-pagos filtro"})

        for i in lista_divs[1:]:
            if i["style"] != "display:none":
                datos_producto = obtener_datos_producto(i)

                dt["Clasificacion"].append(filtro_id)
                dt["Producto"].append(datos_producto["Producto"])
                dt["Precio Actual"].append(datos_producto["Precio Actual"])
                dt["Precio Anterior"].append(datos_producto["Precio Anterior"])
                dt["Forma de pago"].append(datos_producto["Forma de pago"])

    return pd.DataFrame(dt)

"""
PRIMER MENU
"""
if __name__ == "__main__":
    navegador = iniciar_navegador()

    try:
        cargar_pagina(navegador, "https://www.claroshop.com/")
        hacer_clic(navegador, By.XPATH, "//*[@id='__next']/div[1]/header/div[1]/div[2]/div/nav[2]/ul[1]/li[2]/a")
        data_df = filtrado(navegador, ["celulares-y-telefonia-li", "electronica-y-tecnologia-li", "videojuegos-li", "hogar-y-jardin-li",
                             "deportes-y-ocio-li", "ferreteria-y-autos-li", "salud-belleza-y-cuidado-personal-li"])
        data_df.to_csv(data_csv)
        cerrar_navegador(navegador)
        print("Web scraping realizado exitosamente.")

    except Error as error:
        print("Erro al realizar el web scraping:", error)

    try:
        archivo_csv = data_csv
        limpieza = LimpiadorCSV(archivo_csv)
        limpieza.limpieza_duplicados()
        limpieza.limpieza_nulos()
        limpieza.limpieza_de_precio()
        limpieza.extraer_valores_numericos('Forma de pago')
        limpieza.limpiar_forma_de_pago()
        limpieza.signo_de_pesos()
        limpieza.precio_anterior_cero()
        limpieza.cambio_nombre()
        limpieza.guardar_csv(data_limpieza)
        print("Limpieza de datos realizado exitosamente.")

    except Error as error:
        print("Error al realizar la limpieza del archivo csv:", error)

    try:
        db = DataBaseProyecto()
        db.conectar()
        db.crear_base_datos()
        db.crear_tablas()
        db.insertar_datos()
        db.crearquerys()
        db.cerrar_conexion()
        print("Consulta de datos realizada exitosamente.")

    except Error as error:
        print("Error al hacer la conexion con la base de datos:", error)
