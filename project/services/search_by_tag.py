import os

def search_tag(search_term):
    """
    Busca un término específico (tag) en todos los archivos dentro de un directorio de estudio.

    Args:
        search_term (str): Término de búsqueda (tag) que se va a buscar en los archivos.

    Returns:
        None
    """
    # Verificar si se proporciona un argumento
    if not search_term:
        print("Por favor, proporciona un argumento para buscar.")
        return

    # Agregar "#" al inicio del término de búsqueda
    search_term = "#" + search_term

    # Ruta del directorio de estudio
    study_directory = "/home/peace/notes/study"

    # Bucle para iterar sobre los archivos en el directorio
    for file in os.listdir(study_directory):
        file_path = os.path.join(study_directory, file)
        if os.path.isfile(file_path):
            # Verificar si el archivo contiene el término de búsqueda
            with open(file_path, "r", encoding="utf-8") as f:
                if search_term in f.read():
                    # Mostrar la ruta relativa del archivo
                    rel_path = os.path.relpath(file_path, start=study_directory)
                    rel_path = rel_path.replace("_", " ").replace(".md", "")
                    print(f"- {rel_path}")
                    print("")
                    print("")

def main():
    # Argumento de búsqueda
    search_term = input("Introduce el término de búsqueda: ")
    search_tag(search_term)

if __name__ == "__main__":
    main()
