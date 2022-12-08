import pickle
from pathlib import Path
# import streamlit_authenticator as stauth

import streamlit as st
names = ["Kartika", "User"]
usernames = ["kartika", "Usr"]
passwords = ["XXX", "XXX"]

hashed_passwords = st.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
