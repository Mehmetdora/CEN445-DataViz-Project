import streamlit as st
from data_loader import load_dataset
import student_omer
# import student_dora 
import student_ahmet

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="CEN445 Data Viz Project",
    layout="wide",
    initial_sidebar_state="collapsed" # Açılışta yan menüyü gizle
)

# 2. CSS Design
def apply_custom_css():
    st.markdown("""
        <style>
        /* Ana Arka Plan - Modern Koyu Gradyan */
        .stApp {
            background: linear-gradient(to right, #141e30, #243b55);
            color: #ffffff;
        }
        
        /* Başlıklar */
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* Buton Tasarımı - Kart Görünümü */
        .stButton > button {
            width: 100%;
            height: 100px;
            border-radius: 15px;
            background-color: #ffffff;
            color: #243b55;
            border: none;
            font-size: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background-color: #00d2ff;
            color: white;
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        /* Ana Sayfa Dön Butonu (Sidebar) */
        section[data-testid="stSidebar"] .stButton > button {
            height: 50px;
            background-color: #FF4B4B;
            color: white;
        }
        
        /* Bilgi Kutuları */
        .stAlert {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    
    # Oturum Durumu Yönetimi
    # Hangi sayfada olduğumuzu hafızada tutar
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Sayfa Değiştirme Fonksiyonu
    def set_page(page_name):
        st.session_state.current_page = page_name
        # Sayfa değiştiğinde state'i güncellemek için rerun gerekebilir ama 
        # buton callback'leri genellikle otomatik halleder.

    # --- 1. ANA SAYFA (KARŞILAMA EKRANI) ---
    if st.session_state.current_page == "Home":
        st.title("🗽 NYC Airbnb Data Visualization Project")
        st.markdown("### CEN445 - Introduction to Data Visualization")
        st.write("This project is prepared to analyze New York City Airbnb data. Please select the student you want to view:")
        
        st.write("") # Boşluk
        st.write("") 

        # 3 Column Structure (Student Buttons)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("Student 1")
            if st.button("👤 Ömer Faruk Dinçoğlu"):
                set_page("Ömer")
                st.rerun()

        with col2:
            st.info("Student 2")
            if st.button("👤 Student 2"):
                set_page("Student2")
                st.rerun()

        with col3:
            st.info("Student 3")
            if st.button("👤 Ahmet Muhtar Bilal"):
                set_page("Student3")
                st.rerun()
                
        st.divider()
        # Dataset Information
        with st.expander("Dataset Information"):
            df_preview = load_dataset()
            if df_preview is not None:
                st.write(f"Total Listing Count: {len(df_preview)}")
                st.dataframe(df_preview.head())

    # --- 2. ÖĞRENCİ SAYFALARI ---
    else:
        # Her alt sayfada "Geri Dön" butonu olsun
        with st.sidebar:
            st.title("Navigasyon")
            if st.button("🏠 Back to Home"):
                set_page("Home")
                st.rerun()
        
        # Veriyi Yükle (Sadece alt sayfalara girince yüklenir, performans artar)
        df = load_dataset()
        if df is None:
            return

        # --- ÖMER'İN SAYFASI ---
        if st.session_state.current_page == "Ömer":
            # Yan çubuk filtrelerini buraya taşıdık ki sadece bu sayfada görünsün
            st.sidebar.header("Filters (Ömer)")
            all_groups = df['neighbourhood_group'].unique()
            selected_groups = st.sidebar.multiselect("Neighborhood Groups", all_groups, default=all_groups)
            
            # Filtreleme
            df_filtered = df[df['neighbourhood_group'].isin(selected_groups)]
            
            # Modülü Çalıştır
            student_omer.run_omer_module(df_filtered)

        # --- Student 2 SAYFASI ---
        elif st.session_state.current_page == "Student2":
            st.title("👤 Student 2 Analizleri")
            st.warning("Bu modül henüz hazırlanmadı.")
            # student_ali.run_module(df)

        # --- Student 3 SAYFASI ---
        elif st.session_state.current_page == "Student3":
            student_ahmet.run_ahmet_module(df)


if __name__ == "__main__":
    main()
