import requests
import os
from dotenv import load_dotenv


load_dotenv()

# Función para buscar un libro por su título
def buscar_libros_por_titulo(api_key, titulo):
    url = f"https://www.googleapis.com/books/v1/volumes?q={titulo}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}

# Función que te devuelve otros libros que coinciden en parte del título
def mostrar_opciones_libros(datos, titulo):
    if "items" in datos:
        coincidencias_exactas = [libro for libro in datos["items"] if libro["volumeInfo"].get("title", "").lower() == titulo.lower()]
        if coincidencias_exactas:
            libro_exacto = coincidencias_exactas[0]
            mostrar_datos_libro(libro_exacto)
            return []
        else:
            libros = datos["items"][:5]
            opciones = []
            for idx, libro in enumerate(libros):
                titulo_libro = libro["volumeInfo"].get("title", "Título no disponible")
                autores = libro["volumeInfo"].get("authors", ["Autor(es) no disponible(s)"])
                opciones.append((titulo_libro, autores))
                print(f"{idx + 1}. {titulo_libro} - {', '.join(autores)}")
            return opciones
    else:
        print("No se encontraron resultados para el título proporcionado.")
        return []

# Función que te devuelve los datos de los libros
def mostrar_datos_libro(libro):
    titulo = libro["volumeInfo"].get("title", "Título no disponible")
    autores = libro["volumeInfo"].get("authors", ["Autor(es) no disponible(s)"])
    fecha_publicacion = libro["volumeInfo"].get("publishedDate", "Fecha de publicación no disponible")
    descripcion = libro["volumeInfo"].get("description", "Descripción no disponible")

    print(f"\nInformación del libro seleccionado:")
    print(f"Título: {titulo}")
    print(f"Autor(es): {', '.join(autores)}")
    print(f"Fecha de Publicación: {fecha_publicacion}")
    print(f"Descripción: {descripcion}")

# Función principal del programa
def main():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    if not api_key:
        print("La clave de API no está configurada. Por favor, establece la variable de entorno 'GOOGLE_BOOKS_API_KEY'.")
        return

    while True:
        titulo = input("Ingrese el título del libro (o 'salir' para terminar): ")
        if titulo.lower() == 'salir':
            print("Gracias por usar el programa. ¡Adiós!")
            break

        datos = buscar_libros_por_titulo(api_key, titulo)
        if "error" in datos:
            print("Error al buscar los libros:", datos["error"])
            continue

        opciones = mostrar_opciones_libros(datos, titulo)
        if opciones:
            seleccion = int(input("Seleccione el número del libro para ver más detalles: ")) - 1
            if 0 <= seleccion < len(opciones):
                libro_seleccionado = datos["items"][seleccion]
                mostrar_datos_libro(libro_seleccionado)
            else:
                print("Selección inválida.")
        print()

if __name__ == "__main__":
    main()
