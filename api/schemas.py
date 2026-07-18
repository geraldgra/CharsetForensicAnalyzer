from pydantic import BaseModel, HttpUrl, Field


class UrlRequest(BaseModel):

    url: HttpUrl = Field(
        description="URL del archivo a analizar"
    )


class AnalyzeResponse(BaseModel):
    """
    Modelo genérico utilizado únicamente para que
    FastAPI documente correctamente las respuestas.

    El contenido real es construido dinámicamente por
    api.response.success() y api.response.error().
    """

    model_config = {
        "extra": "allow"
    }