import pandas as pd
import pickle  
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import yaml
from yaml import SafeLoader
# --- USER AUTHENTICATION ---

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]
passwords = ['123','456']
# load hashed passwords

credentials = {
        "usernames":{
            "jsmith92":{
                "name":"john smith",
                "password":"$2b$12$TSuKwWML0EpbohBQgHx4p8E5q"
                },
            "tturner":{
                "name":"timmy turner",
                "password":"$2b$12$asdaUduuibuEIyBUBHASD896a"
                }            
            }
 }

with open('config.yaml') as file:
    config = yaml.load(file,Loader=SafeLoader)

authenticator = stauth.Authenticate(
config['credentials'],
config['cookie']['name'],
config['cookie']['key'],
config['cookie']['expiry_days'],
config['preauthorized']
)

hashed_passwords = stauth.Hasher(['123','456']).generate()
authenticator = stauth.Authenticate(names, usernames,hashed_passwords,"sales_dashboard", "abcdef", cookie_expiry_days=30)

# # authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
# authenticator = stauth.Authenticate(names, hashed_passwords, "app_home", "auth", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

    # load the model from disk
    loaded_model = pickle.load(open('tweets_all_data_clean_model.sav', 'rb'))
    loaded_vec= pickle.load(open('vec_model.sav', 'rb'))


    # membaca data berlabel hasil lexicon dan naive bayes
    data = pd.read_csv('tweets_all_data_clean.csv')

    # menampilkan jumlah nilai data label
    neg = data['label'].value_counts()[-1]
    net = data['label'].value_counts()[0]
    pos = data['label'].value_counts()[1]
    data_show= pd.DataFrame(data={'negatif' : [neg], 'positif': [pos], 'netral':[net]})

    # menampilkan judul utama pada web
    st.title('Selamat datang di aplikasi Senasi')
    # menampilkan teks sub judul dan bar chart
    st.subheader('Hasil Sentimen Inflasi dari komentar twitter')
    # Preformatted text
    st.text("This is fixed-width text")
    st.bar_chart(data_show.T) 


    # Membuat prediksi
    st.subheader('Prediksi hasil sentimen inflasi')

    user_input = st.text_input("tweets")

    res = loaded_model.predict(loaded_vec.transform(['coba ngobrolin geopolitik eropa timur dan inflasi turki yg meroket']))

    if st.button('Prediksi'):
        st.write('Hasil Sentimen : ')
        st.write(res[0])