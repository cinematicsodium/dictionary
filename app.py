# from rich.traceback import install
# install(show_locals=True)

import random

import streamlit as st

from dictionarydata import dictionary_data
from translation import Translation
from utils import convert_to_eid


class Dictionary:
    def __init__(self, dictionary_data):
        self.cid_to_category: dict = dictionary_data["cid_to_category"]
        self.eid_to_data: dict[str, dict] = dictionary_data["eid_to_data"]
        self.english_words: list[str] = [
            entry["english"] for entry in self.eid_to_data.values()
        ]

    def initialize(self):
        st.set_page_config(
            page_title="Mescalero Apache Dictionary",
            page_icon="📚",
            layout="centered",
        )
        st.title("Mescalero Apache Dictionary 📚")
        st.html(
            "Search for an <strong>English</strong> word to see its <strong>Mescalero Apache</strong> translation, literal meanings, and category. "
            "<br><br>If there's no exact match, you'll get some similar suggestions."
        )

    def search(self, word: str) -> tuple[str, Translation | None, list[Translation]]:
        eid = convert_to_eid(word)
        primary_result = self.eid_to_data.get(eid)
        if primary_result:
            primary_result = Translation(**primary_result)
            return eid, primary_result, []

        alternatives = []
        for alt_eid, entry in self.eid_to_data.items():
            if eid and (eid.startswith(alt_eid) or alt_eid.startswith(eid)):
                alternatives.append(Translation(**entry))
            elif eid and (alt_eid in eid or eid in alt_eid):
                alternatives.append(Translation(**entry))
            if len(alternatives) >= 20:
                break
        return eid, None, alternatives

    def display_result(self, result: Translation):
        result.mescalero.literal_translations = [
            mt for mt in result.mescalero.literal_translations if mt != result.english
        ]
        w_sfx = "" if len(result.mescalero.words) == 1 else "s"
        t_sfx = "s" if len(result.mescalero.literal_translations) > 1 else ""
        st.write(f"**English Word:** {result.english}")
        st.write(f"**Mescalero Word{w_sfx}:** {'  |  '.join(result.mescalero.words)}")
        if result.mescalero.literal_translations:
            st.write(
                f"**Literal Translation{t_sfx}:** {'  |  '.join(result.mescalero.literal_translations)}"
            )
        st.write(
            f"**Category:** {self.cid_to_category.get(result.cid, 'Unknown Category')}"
        )

    def run(self):
        self.initialize()
        word = st.text_input("Enter a word to search:")
        random_word = st.button("Select a Random Word")
        if random_word:
            selection = random.choice(list(self.eid_to_data.values()))
            translation = Translation(**selection)
            self.display_result(translation)
            return
        if not word:
            return
        eid, primary_result, alternatives = self.search(word)
        if primary_result:
            st.markdown("## Primary Result")
            self.display_result(primary_result)
        elif len(eid) >= 3:
            st.write("No exact match found.")
            if alternatives:
                st.markdown("## Alternative Results")
                st.markdown(f"### Words that contain '{eid}':")
                for result in alternatives:
                    self.display_result(result)
                    st.markdown("---")
        else:
            st.write("No match found. Please try a different word.")


if __name__ == "__main__":
    dictionary = Dictionary(dictionary_data)
    dictionary.run()
