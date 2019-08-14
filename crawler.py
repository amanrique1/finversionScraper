import requests
from bs4 import BeautifulSoup

def main_spider(num_proyectos):
    proyect = 1
    url = 'https://www.metrocuadrado.com/venta/bogota/usado/#'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for link in soup.findAll('a', {'class': "data-details-id"}):
        print("\n" + str(proyect))
        href = link.get('href')
        print(href)
        get_proyect_data(href)
        if proyect == num_proyectos:
            break
        proyect += 1
    print("\nLos proyectos sin precio son: " + str(no_existentes))


def get_proyect_data(proyect_url):
    source_code = requests.get(proyect_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    title = soup.find('div', {'class': "m_property_info_title"}).h1.string
    print("Nombre proyecto:" + title)

    property_info = soup.find('div', {'class': "m_property_info_table"})
    for info in property_info.findAll('dl'):
        clase = info.find('h3').string.strip()
        dato = info.find('dd').string
        if dato is not None:
            print(clase + ": " + dato.strip())
        elif clase == "Área construida":
            dato = str(info.find('dd'))[4:-18].strip()
            print(clase + ": " + dato)

    property_info_details = soup.find('div', {'class': "m_property_info_details"})
    venta_negociable = False
    arriendo_negociable = False
    if property_info_details is not None:
        for info in property_info_details.findAll('dl'):
            clase = info.find('h3').string.strip()
            dato = info.find('h4').string
            if dato is not None:
                print(clase + ": " + dato.strip())
            elif clase == "Área construida" or clase == "Área privada" or clase == "Área del lote":
                dato = str(info.find('dd'))[8:-23].strip()
                print(clase + ": " + dato)
            elif clase == "Valor de venta":
                venta_negociable = True
            elif clase == "Valor de arriendo":
                arriendo_negociable = True
            else:
                print("\n ERROOOOOR en la clase: "+ clase +"AAAAAAAAAAAAAAAAAAAAAAA\n")

        print("Valor venta negociable: " + str(venta_negociable))
        print("Valor arriendo negociable: " + str(arriendo_negociable))

    property_info_details_2 = soup.find('div', {'class': "m_property_info_details more_info"})
    if property_info_details_2 is not None:
        for info in property_info_details_2.findAll('dl'):
            clase = info.find('h3').string.strip()
            dato = info.find('h4').string
            if dato is not None:
                print(clase + ": " + dato.strip())
            else:
                print("\n ERROOOOOR en la clase: "+ clase +"AAAAAAAAAAAAAAAAAAAAAAA\n")

    latitud = soup.find('input', {'id': "latitude"})['value']
    longitude = soup.find('input', {'id': "longitude"})['value']
    print("latitud :" + latitud)
    print("longitude :" + longitude)


no_existentes = 0
main_spider(100)
