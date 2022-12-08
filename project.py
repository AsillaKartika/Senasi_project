import pandas as pd
import pickle  
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import yaml
from yaml import SafeLoader
# --- USER AUTHENTICATION ---

names = ["User", "Testing", "Kartika"]
usernames = ["user", "testing", "kartika"]
passwords = ['123','456', '140']
# load hashed passwords

credentials = {
        "usernames":{
            "kartika":{
                "name":"Kartika",
                "password":"140"
                },
            "tturner":{
                "name":"user",
                "password":"123"
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
    loaded_model = pickle.load(open('tweets_data_labeled_model.sav', 'rb'))
    loaded_vec= pickle.load(open('vec_model.sav', 'rb'))


    # membaca data berlabel hasil lexicon dan naive bayes
    data = pd.read_csv('tweets_data_labeled.csv')

    # menampilkan jumlah nilai data label
    neg = data['label'].value_counts()[-1]
    net = data['label'].value_counts()[0]
    pos = data['label'].value_counts()[1]
    data_show= pd.DataFrame(data={'negatif' : [neg], 'positif': [pos], 'netral':[net]})

    # menampilkan judul utama pada web
    st.title('Selamat datang di aplikasi Senasi')
    # menampilkan teks sub judul dan bar chart
    st.subheader('Sentimen Inflasi dari komentar twitter')
    # Preformatted text
    st.write("Sentiment analysis biasa digunakan untuk melihat pendapat atau kecenderungan opini terhadap sebuah masalah atau objek oleh seseorang menuju ke opini positif atau negatif.")
    st.write('Sedangkan Inflasi adalah suatu keadaan dimana tingkat harga umum (price level) cenderung naik yang disebabkan oleh peningkatan permintaan yang melebihi penawaran atau kapasitas produksi, sehingga menyebabkan kenaikan harga (demand-pull inflation). Inflasi dapat terjadi atau dapat juga disebabkan oleh sisi penawaran yaitu kenaikan biaya produksi. Oleh karena itu, kenaikan harga (biaya) dapat meningkatkan inflasi).')
    st.subheader('Dibawah ini merupakan tabel dari hasil sentimen analisis komentar twitter yang berkaitan dengan inflasi:')
    st.bar_chart(data_show.T) 


    # Membuat prediksi
    st.subheader('Prediksi hasil sentimen inflasi')

    user_input = st.text_input("tweets")

    res = loaded_model.predict(loaded_vec.transform([' ']))

    if st.button('Prediksi'):
        st.text('Hasil Sentimen : ')
        st.write(res[0])
