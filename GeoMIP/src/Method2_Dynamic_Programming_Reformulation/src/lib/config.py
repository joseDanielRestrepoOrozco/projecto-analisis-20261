import os

"""Carga y exporta variables de entorno para definir que archivos se van a usar en el programa. Estas variables se pueden definir en un archivo .env o directamente en el entorno de ejecución."""

SAMPLE_LETTER: str = os.getenv("GEOMIP_SAMPLE_LETTER", "C")
INITIAL_STATE: str = os.getenv("GEOMIP_INITIAL_STATE", "100")
CONDITIONS: str | None = os.getenv("GEOMIP_CONDITIONS")
SCOPE: str | None = os.getenv("GEOMIP_SCOPE")
MECHANISM: str | None = os.getenv("GEOMIP_MECHANISM")
TPM_PATH: str | None = os.getenv("GEOMIP_TPM_PATH")

def resolve_config() -> dict[str, str | None]:
    n = len(INITIAL_STATE)
    return {
        "sample_letter": SAMPLE_LETTER,
        "initial_state": INITIAL_STATE,
        "conditions": CONDITIONS if CONDITIONS is not None else "1" * n,
        "scope": SCOPE if SCOPE is not None else "1" * n,
        "mechanism": MECHANISM if MECHANISM is not None else "1" * n,
        "tpm_path": TPM_PATH,
    }
