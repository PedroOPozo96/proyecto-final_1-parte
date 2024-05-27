import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Función para buscar los libros por el nombre del autor
def buscar_libros_por_autor(api_key, autor, start_index=0, max_results=5):
    url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{autor}&startIndex={start_index}&maxResults={max_results}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}

# Función que te devuelve los libros buscados del autor.
def mostrar_libros(datos, autor, start_index):
    if "items" in datos:
        autores_encontrados = set()
        for libro in datos["items"]:
            autores = libro["volumeInfo"].get("authors", ["Autor no disponible"])
            for a in autores:
                autores_encontrados.add(a.lower())

        nombre_concreto = len(autores_encontrados) == 1

        print(f"\nLibros de autores que coinciden con '{autor}':")
        libros_mostrados = 0
        for idx, libro in enumerate(datos["items"]):
            titulo = libro["volumeInfo"].get("title", "Título no disponible")
            autores = libro["volumeInfo"].get("authors", ["Autor no disponible"])
            if libros_mostrados < 5:
                if nombre_concreto:
                    print(f"{start_index + libros_mostrados + 1}. {titulo}")
                else:
                    print(f"{start_index + libros_mostrados + 1}. {titulo} - {', '.join(autores)}")
                libros_mostrados += 1

        total_libros = datos.get("totalItems", 0)
        if start_index + 5 < total_libros:
            return True 
        else:
            return False  
    else:
        print("No se encontraron resultados para el autor proporcionado.")
        return False

# Función que te devuelve la descripción sobre un autor
def obtener_descripcion_autor(api_key, autor):
    start_index = 0
    max_results = 10
    while start_index < 100:  
        datos = buscar_libros_por_autor(api_key, autor, start_index=start_index, max_results=max_results)
        if "items" in datos:
            for libro in datos["items"]:
                descripcion = libro["volumeInfo"].get("description", "")
                if descripcion and (autor.lower() in descripcion.lower() or "autor" in descripcion.lower() or "biografía" in descripcion.lower()):
                    return descripcion
        start_index += max_results
    return "No se encontró una biografía del autor en la información disponible."

# Función principal del programa
def main():
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    if not api_key:
        print("La clave de API no está configurada. Por favor, establece la variable de entorno 'GOOGLE_BOOKS_API_KEY' en el archivo .env.")
        return

    while True:
        autor = input("Ingrese el nombre del autor o 'salir' para cerrar el programa: ")
        if autor.lower() == 'salir':
            print("Gracias por usar el programa. ¡Adiós!")
            break

        descripcion_autor = obtener_descripcion_autor(api_key, autor)
        print(f"\nDescripción del autor '{autor}':\n{descripcion_autor}")

        ver_libros = input("¿Desea ver la lista de libros de este autor? (sí/no): ")
        if ver_libros.lower() == 'sí':
            start_index = 0
            while True:
                datos = buscar_libros_por_autor(api_key, autor, start_index=start_index, max_results=5)
                if "error" in datos:
                    print("Error al buscar los libros:", datos["error"])
                    break

                hay_mas_libros = mostrar_libros(datos, autor, start_index)
                if not hay_mas_libros:
                    break

                ver_mas = input("¿Desea ver más libros de este autor? (sí/no): ")
                if ver_mas.lower() == 'sí':
                    start_index += 5
                else:
                    break

        print()

if __name__ == "__main__":
    main()
