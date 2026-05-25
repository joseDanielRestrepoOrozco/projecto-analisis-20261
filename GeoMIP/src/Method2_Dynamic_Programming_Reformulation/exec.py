from src.models.base.application import aplicacion
from src.controllers.manager import Manager
from src.controllers.strategies.geometric import GeometricSIA
from src.lib.config import resolve_config
import numpy as np

def main():
    cfg = resolve_config()

    aplicacion.profiler_habilitado = True
    aplicacion.pagina_sample_network = cfg["sample_letter"]

    estado_inicial = cfg["initial_state"]
    condiciones = cfg["conditions"]
    alcance = cfg["scope"]
    mecanismo = cfg["mechanism"]

    gestor = Manager(estado_inicial)
    tpm_path = cfg["tpm_path"] or gestor.tpm_filename
    tpm = np.genfromtxt(tpm_path, delimiter=",")

    print(f"Analizando red: {tpm_path}")
    print(f"TPM:\n{tpm}")
    print(f"Estado inicial: {estado_inicial}")
    print(f"Condiciones: {condiciones}, Alcance: {alcance}, Mecanismo: {mecanismo}")

    analizador = GeometricSIA(gestor)
    solucion = analizador.aplicar_estrategia(
        condiciones,
        alcance,
        mecanismo,
        tpm,
    )
    print(solucion)


if __name__ == "__main__":
    main()
