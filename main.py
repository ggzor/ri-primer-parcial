from re import compile
from pathlib import Path
from nltk.stem.porter import PorterStemmer

# Constantes utilizadas
SIGNOS_PUNTUACION = ".,;:¿?¡!()[]/\\'\"&-_►—%@…|’“”"
NUMEROS = "0123456789"
RE_PALABRA = compile(r"\b[a-zñáéíóú]+\b")

# Crear el truncador de PorterStemmer
truncador = PorterStemmer()

# Función para terminar en caso de error
def exitError(mensaje):
    print(mensaje)
    exit(1)


# Archivos y carpetas utilizados
originales = Path("originales")
pasos = Path("pasos")
procesados = Path("procesados")
archivo_stopwords = Path("stopwords.txt")

# Verificación de existencia de archivos
if not originales.exists():
    exitError(
        "No se localizó la carpeta con"
        " los documentos originales: \n" + str(originales.absolute())
    )
if not archivo_stopwords.exists():
    exitError(
        "No se localizó el archivo de palabras cerradas:\n" + str(archivo_stopwords)
    )

# Crear carpeta de salida
if not procesados.exists():
    procesados.mkdir()

if not pasos.exists():
    pasos.mkdir()

# Cargar las palabras cerradas
stopwords = set(archivo_stopwords.read_text("utf-8").split("\n"))

# Procesar cada documento
for documento in sorted(originales.iterdir()):
    archivo_pasos = pasos / documento.name

    with open(archivo_pasos, "w") as archivo:
        t = documento.read_text("utf-8")
        print(documento, file=archivo)
        print("Original: \n", t, file=archivo)

        for s in SIGNOS_PUNTUACION:
            t = t.replace(s, " ")
        print("Sin signos de puntuación: \n", t, file=archivo)

        for n in NUMEROS:
            t = t.replace(n, "")
        print("Sin números: \n", t, file=archivo)

        t = t.lower()
        print("Minúsculas: \n", t, file=archivo)

        t = RE_PALABRA.findall(t)
        print("Palabras: \n", t, file=archivo)

        print(file=archivo)
        t = [p for p in t if p not in stopwords]
        print("Sin cerradas: \n", t, file=archivo)

        print(file=archivo)
        t = [truncador.stem(p) for p in t]
        print("Truncadas: \n", t, file=archivo)

        print(file=archivo)
        t = " ".join(t)
        print("Texto final: \n", t, file=archivo)

        documento_final = procesados / documento.name
        documento_final.write_text(t, encoding="utf-8")
