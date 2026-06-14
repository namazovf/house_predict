import streamlit as st
st.set_page_config(page_title='Ev Elanı Proqnozu', page_icon='🏠', layout='centered')
import pandas as pd
import numpy as np
import joblib

model = joblib.load('binaaz_best_model.pkl')

st.title('🏠 Ev Elanı Çıxarış Proqnozu')
st.write('Aşağıdakı məlumatları daxil edin:')

col1, col2 = st.columns(2)

with col1:
    price = st.number_input('Qiymət (AZN)', min_value=1000, max_value=10000000, value=100000)
    city = st.selectbox('Şəhər', ['Bakı', 'Gəncə', 'Sumqayıt', 'Lənkəran', 'Digər'])
    otaq = st.number_input('Otaq sayı', min_value=1, max_value=20, value=3)
    sahe = st.number_input('Sahə (m²)', min_value=10, max_value=1000, value=80)

with col2:
    mertebe_cur = st.number_input('Mərtəbə', min_value=1, max_value=50, value=5)
    mertebe_total = st.number_input('Binanın mərtəbə sayı', min_value=1, max_value=50, value=9)
    temir = st.selectbox('Təmir', ['var', 'yox'])
    kateqoriya = st.selectbox('Kateqoriya', ['Yeni tikili', 'Köhnə tikili', 'Həyət evi', 'Villa'])

if st.button('Proqnoz et'):
    sahe_num = sahe
    price_per_m2 = price / (sahe_num + 1)
    is_top_floor = int(mertebe_cur == mertebe_total)
    is_ground_floor = int(mertebe_cur == 1)
    floor_ratio = mertebe_cur / (mertebe_total + 1)
    repair_bin = int(temir == 'var')

    input_df = pd.DataFrame([{
        'price': price,
        'Sahə_num': sahe_num,
        'Otaq sayı': otaq,
        'mertebe_cur': mertebe_cur,
        'mertebe_total': mertebe_total,
        'lat': 40.4093,
        'lng': 49.8671,
        'views': 0,
        'price_per_m2': price_per_m2,
        'floor_ratio': floor_ratio,
        'is_top_floor': is_top_floor,
        'is_ground_floor': is_ground_floor,
        'vip': 0,
        'featured': 0,
        'bill_of_sale': 0,
        'repair_bin': repair_bin,
        'Kateqoriya': kateqoriya,
        'city': city
    }])

    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    if pred == 1:
        st.success(f'✅ Çıxarış var! Ehtimal: {prob:.1%}')
    else:
        st.error(f'❌ Çıxarış yoxdur. Ehtimal: {prob:.1%}')
