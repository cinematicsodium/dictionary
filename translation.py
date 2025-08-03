class Mescalero:
    def __init__(self, data: dict):
        self.literal_translations: list[str] = data.get("literal_translations", [])
        self.words: list[str] = data.get("words", [])


class Translation:
    def __init__(self, data: dict):
        self.cid: str = data.get("cid", "")
        self.eid: str = data.get("eid", "")
        self.english: str = data.get("english", "")
        self.mescalero: Mescalero = Mescalero(data.get("mescalero", {}))
