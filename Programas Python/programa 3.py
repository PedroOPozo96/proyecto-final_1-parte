import requests


#Función que busca los libros ingresando el género

def buscar_libros_por_genero(api_key, genero, start_index=0, max_results=5):
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genero}&startIndex={start_index}&maxResults={max_results}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}
    

# Con esta función nos devuelve la edad dedicada del libro

def es_infantil_o_juvenil(categorias, descripcion):
    if not categorias:
        categorias = []
    categorias = [cat.lower() for cat in categorias]
    descripcion = descripcion.lower() if descripcion else ""
    
    infantil_keywords = ['children', 'kids', 'young readers', 'juvenile']
    juvenil_keywords = ['teen', 'young adult', 'adolescent', 'juvenile fiction']

    for keyword in infantil_keywords:
        if keyword in categorias or keyword in descripcion:
            return "Infantil"
    
    for keyword in juvenil_keywords:
        if keyword in categorias or keyword in descripcion:
            return "Juvenil"
    
    return "Adulto"


#Esta función nos devuelve los libros cuando ingresamos un género 

def mostrar_libros_por_genero(datos, genero, start_index):
    if "items" in datos:
        print(f"\nLibros en el género '{genero}':")
        libros_mostrados = 0
        for idx, libro in enumerate(datos["items"]):
            titulo = libro["volumeInfo"].get("title", "Título no disponible")
            autores = libro["volumeInfo"].get("authors", ["Autor no disponible"])
            categorias = libro["volumeInfo"].get("categories", [])
            descripcion = libro["volumeInfo"].get("description", "")
            edad = es_infantil_o_juvenil(categorias, descripcion)
            if libros_mostrados < 5:
                print(f"{start_index + libros_mostrados + 1}. {titulo} - {', '.join(autores)} - {edad}")
                libros_mostrados += 1

        total_libros = datos.get("totalItems", 0)
        if start_index + 5 < total_libros:
            return True 
        else:
            return False 
    else:
        print("No se encontraron resultados para el género proporcionado.")
        return False

def main():
    API_KEY = "AIzaSyD3783cwb-UwTnNx1_5U7_JNBGKHHc8TTg"

    while True:
        genero = input("Ingrese el género de los libros que desea buscar (o 'salir' para terminar): ")
        if genero.lower() == 'salir':
            print("Gracias por usar el programa. ¡Adiós!")
            break

        start_index = 0
        while True:
            datos = buscar_libros_por_genero(API_KEY, genero, start_index=start_index, max_results=5)
            if "error" in datos:
                print("Error al buscar los libros:", datos["error"])
                break

            hay_mas_libros = mostrar_libros_por_genero(datos, genero, start_index)
            if not hay_mas_libros:
                break

            ver_mas = input("¿Desea ver más libros de este género? (sí/no): ")
            if ver_mas.lower() == 'sí':
                start_index += 5
            else:
                break

        print()

if __name__ == "__main__":
    main()
