import os
import pandas as pd

DATA_PATH = r"data"


def cargar_csv(ruta):
    """
    Carga un archivo CSV desde una ruta especificada.

    Parameters
    ----------
    ruta : str
        Ruta del archivo CSV.

    Returns
    -------
    pandas.DataFrame
        DataFrame cargado.
    """

    try:
        return pd.read_csv(ruta)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )


def listar_csv():
    """
    Lista todos los archivos CSV disponibles
    en la carpeta data.

    Returns
    -------
    list[str]
        Lista de archivos CSV.
    """

    return [
        archivo
        for archivo in os.listdir(DATA_PATH)
        if archivo.endswith(".csv")
    ]


def seleccionar_csv():
    """
    Permite seleccionar un dataset desde consola.

    Returns
    -------
    str
        Ruta completa del archivo seleccionado.
    """

    archivos = listar_csv()

    if not archivos:
        raise FileNotFoundError(
            "No se encontraron archivos CSV en la carpeta data."
        )

    print("\n=== DATASETS DISPONIBLES ===")

    for i, archivo in enumerate(
        archivos,
        start=1
    ):
        print(f"{i}. {archivo}")

    while True:
        try:
            opcion = int(
                input(
                    "\nSeleccione un dataset: "
                )
            )

            if 1 <= opcion <= len(archivos):
                return os.path.join(
                    DATA_PATH,
                    archivos[opcion - 1]
                )

            print("Opción inválida.")

        except ValueError:
            print(
                "Ingrese un número válido."
            )