import os
from collections import defaultdict

class NotesChecker:
    """Clase para verificar el estado de las notas."""

    def __init__(self, carpeta: str):
        """Inicializa el objeto NotesChecker con la carpeta especificada."""
        self._carpeta_completa = os.path.expanduser(carpeta)
        self._archivos_md = self._obtener_archivos_md()
        self._carpeta = carpeta

    def _obtener_archivos_md(self):
        """Obtiene todos los archivos .md en la carpeta y subcarpetas."""
        archivos_md = []
        for carpeta_actual, _, archivos in os.walk(self._carpeta_completa):
            for archivo in archivos:
                if archivo.endswith(".md"):
                    archivos_md.append(os.path.join(carpeta_actual, archivo))
        if not archivos_md:
            raise ValueError("No se encontraron archivos .md en la carpeta.")
        return archivos_md

    def filtrar_archivos_sin_tags(self):
        """Filtra los archivos .md que no tienen tags."""
        archivos_sin_tags = []
        vacios = []
        for archivo_md in self._archivos_md:
            with open(archivo_md, 'r', encoding='utf-8') as archivo:
                contenido = archivo.readlines()
                if not contenido:
                    archivos_sin_tags.append(archivo_md)
                    vacios.append(archivo_md)
                else:
                    linea = contenido[-1]
                    lista_con_tags = [word.removesuffix("\n") for word in linea.split(" ") if word.startswith('#', 0, 1)]
                    lista_con_tags = [tag for tag in lista_con_tags if tag != '#']
                    lista_con_tags = [tag for tag in lista_con_tags if tag[1] != '#']
                    if not lista_con_tags:
                        archivos_sin_tags.append(archivo_md)
        return archivos_sin_tags, vacios

    def contar_frecuencia_tags(self):
        """Cuenta la frecuencia de cada tag en todos los archivos .md."""
        contador_tags = defaultdict(int)
        for archivo_md in self._archivos_md:
            with open(archivo_md, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                tags = [tag for tag in contenido.split() if tag.startswith('#') and not tag.endswith('#')]
                for tag in tags:
                    contador_tags[tag] += 1
        return contador_tags

    def listar_archivos_sin_tags(self, archivos_sin_tags):
        """Lista los archivos sin tags de la carpeta de notas."""
        print("\n## Notas sin tags:\n")
        for archivo in archivos_sin_tags:
            print(archivo.replace(self._carpeta_completa, ""))

    def listar_notas_vacias(self, vacios):
        """Lista las notas vacías de la carpeta de notas."""
        print("\n## Notas vacías:\n")
        for vacio in vacios:
            print(f"Vacia: {vacio}")

    def reporte_general(self, archivos_sin_tags, vacios):
        """Imprime el reporte general del estado de las notas."""
        vacios_con_conten = len(archivos_sin_tags) - len(vacios)
        print(f"\n==Notas sin tag: {len(archivos_sin_tags)} en total")
        print(f"==Notas sin tag con contenido: {vacios_con_conten}")
        print(f"==Notas vacías: {len(vacios)}\n")

    def listar_tags_y_frecuencia(self, contador_tags):
        """Lista los tags en uso y su frecuencia."""
        print(f"\n## Tags en uso ({len(contador_tags.keys())}) en total:\n")
        for tag, frecuencia in sorted(contador_tags.items(), key=lambda x: x[1], reverse=True):
            print(f"{tag}: {frecuencia}")

class UI:
    """Clase para la interfaz de usuario."""

    def __init__(self, service: NotesChecker):
        """Inicializa el objeto UI con el servicio NotesChecker."""
        self._service = service

    def informar_estudiante(self, archivos_sin_tags, vacios):
        """Muestra el estado de las notas al estudiante."""
        print("NOTES!")
        print("Utilidad para revisar el estado actual de las notas.\n")
        print("Veamos las notas vacías...\n")
        self._service.reporte_general(archivos_sin_tags, vacios)

    def preguntar_estudiante(self, archivos_sin_tags, vacios):
        """Pregunta al estudiante si desea ver las notas vacías y sin tags."""
        if len(vacios) > 0:
            o1 = input(f"Desea listar las {len(vacios)} notas vacías? (s/n)")
            if o1.upper() == "S":
                self._service.listar_notas_vacias(vacios)

        if len(archivos_sin_tags) > 0:
            o1 = input(f"Desea listar las {len(archivos_sin_tags)} notas sin tags? (s/n)")
            if o1.upper() == "S":
                self._service.listar_archivos_sin_tags(archivos_sin_tags)

        contador_tags = self._service.contar_frecuencia_tags()
        o1 = input(f"Desea listar los ({len(contador_tags)}) tags y sus frecuencias? (s/n)")
        if o1.upper() == "S":
            self._service.listar_tags_y_frecuencia(contador_tags)

def main():
    """Función principal para ejecutar el programa."""
    carpeta = "~/notes/study"
    service = NotesChecker(carpeta)
    ui = UI(service)
    archivos_sin_tags, vacios = service.filtrar_archivos_sin_tags()
    ui.informar_estudiante(archivos_sin_tags, vacios)
    ui.preguntar_estudiante(archivos_sin_tags, vacios)

if __name__ == "__main__":
    main()
