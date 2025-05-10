import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="House Listings Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("house_listings.csv")
    df['price'] = df['price'].str.replace(" ", "").str.replace("AZN", "").astype(float)
    df['area_m2'] = df['area'].str.replace(" m²", "").astype(float)
    df['price_1m2'] = df['price_1m2'].str.extract(r'(\d+)').astype(float)
    df['room_number'] = df['room_number'].fillna(0).astype(int)
    return df

df = load_data()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Descriptives", "Sales", "Profit"])

# Dataset download from sidebar
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Dataseti yüklə",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='house_listings.csv',
    mime='text/csv'
)

# Main content
if page == "Descriptives":
    st.title("Tikili növünə görə ümumi baxış")
    st.subheader("Orta qiymət və say")

    avg_price = df.groupby('category')['price'].mean().reset_index()
    count_by_cat = df['category'].value_counts().reset_index()
    count_by_cat.columns = ['category', 'count']

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(avg_price, x='category', y='price', title="Orta qiymət", color='category')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(count_by_cat, x='category', y='count', title="Elan sayı", color='category')
        st.plotly_chart(fig2, use_container_width=True)

elif page == "Sales":
    st.title("Otaq sayına görə 1 m² qiymət analizi")
    avg_price_room = df.groupby('room_number')['price_1m2'].mean().reset_index()
    fig = px.bar(
        avg_price_room,
        x='room_number',
        y='price_1m2',
        title="Otaq sayına görə orta 1 m² qiymət",
        labels={'room_number': 'Otaq sayı', 'price_1m2': '1 m² qiymət'},
        color='price_1m2'
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Profit":
    st.title("Rayonlara görə orta qiymət")

    # Rayon adlarını address sütunundan çıxarırıq
    df['rayon'] = df['address'].str.extract(r',\s*([^,]+?)(?:\s+m\.)?$')
    avg_price_rayon = df.groupby('rayon')['price'].mean().reset_index().dropna()

    fig = px.bar(
        avg_price_rayon.sort_values('price', ascending=False),
        x='rayon',
        y='price',
        title="Rayonlara görə orta satış qiyməti",
        labels={'rayon': 'Rayon', 'price': 'Orta qiymət (AZN)'},
        color='price'
    )
    st.plotly_chart(fig, use_container_width=True)

# Download section in main area
st.markdown("---")
st.subheader("Mövcud datasetin yüklənməsi")
st.download_button(
    label="📥 Dataseti yüklə (CSV)",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='house_listings.csv',
    mime='text/csv'
)