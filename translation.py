from pydantic import BaseModel


class Mescalero(BaseModel):
    literal_translations: list[str]
    words: list[str]


class Translation(BaseModel):
    cid: str
    eid: str
    english: str
    mescalero: Mescalero
