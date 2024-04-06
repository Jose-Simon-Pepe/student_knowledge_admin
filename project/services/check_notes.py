import os
from collections import defaultdict

# Función para obtener todos los archivos .md en la carpeta y subcarpetas
def obtener_archivos_md(carpeta):
    archivos_md = []
    carpeta_completa = os.path.expanduser(carpeta)
    for ruta_carpeta, _, archivos in os.walk(carpeta_completa):
        for archivo in archivos:
            if archivo.endswith(".md"):
                archivos_md.append(os.path.join(ruta_carpeta, archivo))
    return archivos_md

# Función para filtrar archivos .md que no tienen tags
def filtrar_archivos_sin_tags(archivos_md):
    archivos_sin_tags = []
    vacios = []
    for archivo_md in archivos_md:
        with open(archivo_md, 'r', encoding='utf-8') as archivo:
            contenido = archivo.readlines()
            if len(contenido) == 0:
                archivos_sin_tags.append(archivo_md)
                vacios.append(archivo_md)
            else:
                linea = contenido[len(contenido)-1]
                lista_con_tags = [word.removesuffix("\n") for word in linea.split(" ") if word.startswith('#', 0, 1)]
                lista_con_tags = [tag for tag in lista_con_tags if not tag[1]=='#']
                if len(lista_con_tags) == 0:
                    archivos_sin_tags.append(archivo_md)
    return archivos_sin_tags, vacios

# Función para contar la frecuencia de cada tag en todos los archivos .md
def contar_frecuencia_tags(archivos_md):
    contador_tags = defaultdict(int)
    for archivo_md in archivos_md:
        with open(archivo_md, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            tags = [tag for tag in contenido.split() if tag.startswith('#') and not tag.endswith('#')]
            for tag in tags:
                contador_tags[tag] += 1
    return contador_tags

def main():
    carpeta = "~/notes/study"
    archivos_md = obtener_archivos_md(carpeta)

    # Filtrar archivos .md que no tienen tags
    archivos_sin_tags, vacios = filtrar_archivos_sin_tags(archivos_md)

    print("NOTES!")
    print("Utilidad para revisar el estado actual de las notas.")
    print("")
    print("Veamos las notas vacias...")
    print("")
    
    # Imprimir la lista de archivos sin tags
    print(f"==Notas sin tag: {len(archivos_sin_tags)} en total")
    vacios_con_conten = len(archivos_sin_tags) - len(vacios)
    print(f"==Notas sin tag con contenido: {vacios_con_conten}")
    print(f"==Notas vacias: {len(vacios)}")
    print("")
    o1 = input(f"Desea listar las notas vacias? ({len(vacios)}) (s/n)")
    if o1.upper() == "S":
        print("")
        print("## Notas vacias:")
        print("")
        for vacio in vacios:
            print(f"Vacia: {vacio}")

    untag = len(archivos_sin_tags)
    o1 = input(f"Desea listar las notas sin tags? {untag} (s/n)")
    if o1.upper() == "S":
        print("")
        print("## Notas sin tags:")
        print("")
        for archivo in archivos_sin_tags:
            print(archivo.replace(carpeta_completa, ""))

    # Contar la frecuencia de cada tag en todos los archivos .md
    contador_tags = contar_frecuencia_tags(archivos_md)

    o1 = input(f"Desea listar los tags ({len(contador_tags)}) y sus frecuencias? (s/n)")
    if o1.upper() == "S":
        print("")
        print(f"## Tags en uso ({len(contador_tags.keys())}) en total:")
        print("")
        for tag, frecuencia in sorted(contador_tags.items(), key=lambda x: x[1], reverse=True):
            print(f"{tag}: {frecuencia}")

if __name__ == "__main__":
    main()
