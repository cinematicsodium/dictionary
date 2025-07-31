# from rich.traceback import install
# install(show_locals=True)

import streamlit as st
from dictionarydata import dictionary_data
from utils import convert_to_eid


class Dictionary:
    def __init__(self, dictionary_data):
        self.data: dict = dictionary_data
        self.cid_to_category: dict = self.data["cid_to_category"]
        self.eid_to_data: dict[str, dict] = self.data["eid_to_data"]
        self.eid = ""
        self.primary_result: dict = {}
        self.alternative_results: list = []


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

    def primary_search(self):
        word = st.text_input("Enter a word to search:")
        if word:
            self.eid = convert_to_eid(word)
            found_entry = self.eid_to_data.get(self.eid)
            if found_entry:
                self.primary_result = found_entry
            else:
                return

    def secondary_search(self):
        eid_by_prefix = []
        alternative_eids = []

        for eid in self.eid_to_data:
            if self.eid.startswith(eid) or eid.startswith(self.eid):
                eid_by_prefix.append(eid)
            elif eid in self.eid or self.eid in eid:
                alternative_eids.append(eid)

        eid_by_prefix.extend(alternative_eids)
        for idx, eid in enumerate(eid_by_prefix):
            if idx < 10:
                result = self.eid_to_data[eid]
                self.alternative_results.append(result)

    def unpack_result(self, result: dict) -> list:
        cid = result.get("CID")
        category = self.cid_to_category.get(cid, "Unknown Category")
        english_word = result["english"]
        mescalero_data = result["mescalero"]
        ms_words = mescalero_data["words"]
        ms_literal_translations = mescalero_data["literal_translations"]
        return [english_word, ms_words, ms_literal_translations, category]

    def display_result(self, result):
        unpacked = self.unpack_result(result)
        en_word, ms_words, ms_translations, category = unpacked
        word = "Word" if len(ms_words) == 1 else "Words"
        st.write(f"**English Word:** {en_word}")
        st.write(f"**Mescalero {word}:** {'  |  '.join(ms_words)}")
        ms_translations = [mt for mt in ms_translations if mt != en_word]
        if ms_translations:
            st.write(
                f"**Mescalero Literal Translations:** {'  |  '.join(ms_translations)}"
            )
        st.write(f"**Category:** {category}")

    def display_primary_result(self):
        st.subheader("Primary Result")
        self.display_result(self.primary_result)

    def display_alternative_results(self):
        st.subheader("Alternative Results")
        for result in self.alternative_results:
            self.display_result(result)
            st.write("---")

    def run(self):
        self.initialize()
        self.primary_search()
        if not self.eid:
            return

        elif self.primary_result:
            self.display_primary_result()
            return

        elif len(self.eid) >= 3:
            st.write("No exact match found. Searching for similar entries...")
            self.secondary_search()
            if self.alternative_results:
                self.display_alternative_results()
            else:
                st.write("No similar entries found. Please try a different word.")
        else:
            st.write("No match found. Please try a different word.")


if __name__ == "__main__":
    dictionary = Dictionary(dictionary_data)
    dictionary.run()
