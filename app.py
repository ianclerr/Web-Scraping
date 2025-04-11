from bs4 import BeautifulSoup as bs
import undetected_chromedriver as uc
import pandas as pd
import time

# Iniciar navegador
browser = uc.Chrome()

# URL de la página
url = "https://www.chacomer.com.py/moto/kenton.html?tipo_de_moto%5B0%5D=TRAIL&tipo_de_moto%5B1%5D=CUB%2FMOTONETA&tipo_de_moto%5B2%5D=SCOOTER&tipo_de_moto%5B3%5D=RUTERA&tipo_de_moto%5B4%5D=CUB%2F+MOTONETA&tipo_de_moto%5B5%5D=UTILITARIA&tipo_de_moto%5B6%5D=EL%C3%89CTRICA"
browser.get(url)
time.sleep(5)  # Esta linea espera a que cargue el contenido

html = browser.page_source
soup = bs(html, 'lxml')

# Crear listas para guardar datos
nombres = []
precios = []
cuotas = []
links = []

# Buscar los productos por su clase
productos = soup.find_all('div', class_='product details product-item-details')

for producto in productos:
    # Nombre y enlace
    nombre_tag = producto.find('strong', class_='product name product-item-name')
    nombre = nombre_tag.text.strip() if nombre_tag else 'No encontrado'
    link = nombre_tag.a['href'] if nombre_tag and nombre_tag.a else 'Sin link'

    # Precio
    precio_tag = producto.find('span', class_='price')
    precio = precio_tag.text.strip() if precio_tag else 'No encontrado'

    # Cuota seleccionada
    select_tag = producto.find('select', class_='installments')
    cuota_seleccionada = select_tag.find('option', selected=True).text.strip() if select_tag else 'No encontrada'

    # Guardar en las listas
    nombres.append(nombre)
    precios.append(precio)
    cuotas.append(cuota_seleccionada)
    links.append(link)

# Crear el DataFrame
df = pd.DataFrame({
    'Nombre': nombres,
    'Precio': precios,
    'Cuota (seleccionada)': cuotas,
    'Link': links
})

# Mostrar el resultado
print(df)
