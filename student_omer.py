import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def run_omer_module(df):
    """
    Ömer Faruk Dinçoğlu'nun grafiklerini çizen ana fonksiyon.
    df: Ana veri çerçevesi (app.py'den gelir)
    """
    st.header("👤 Ömer Faruk Dinçoğlu'nun Analizleri")
    st.markdown("""
    Bu bölümde **Fiyat Dağılımı**, **Pazar Hiyerarşisi** ve **Oda Tipi Kompozisyonu** analiz edilmektedir.
    """)
    
    # --- Yan Çubuk Filtreleri (Sadece bu sayfa için geçerli olabilir veya globalden gelebilir) ---
    # Burada global filtreleri kullanmak daha mantıklı olduğu için filtreleri app.py'den gelen
    # filtrelenmiş veri (df) üzerinde uygulayacağız.
    
    st.divider()

    # --- GRAFİK 1: Fiyat Dağılım Analizi (Histogram) ---
    st.subheader("1. Fiyat Dağılım Analizi (Histogram)")
    st.info("Soru: New York genelindeki fiyatlar nasıl dağılıyor? Çoğunluk hangi aralıkta?")
    
    # Fiyat filtresi (Histogramın anlamlı olması için aşırı uçları kesmek gerekebilir)
    # Kullanıcıya interaktiflik sunalım
    max_price_filter = st.slider("Histogram için Maksimum Fiyat Sınırı", 100, 2000, 500)
    df_hist = df[df['price'] <= max_price_filter]

    fig_hist = px.histogram(
        df_hist, 
        x="price", 
        nbins=50, 
        title=f"{max_price_filter}$ Altındaki İlanların Fiyat Dağılımı",
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(xaxis_title="Fiyat ($)", yaxis_title="İlan Sayısı")
    st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()

    # --- GRAFİK 4: Pazarın Hiyerarşik Yapısı (Treemap) ---
    st.subheader("2. Pazarın Hiyerarşik Yapısı (Treemap)")
    st.info("Soru: Hangi bölge ve semtler pazarın ne kadarını oluşturuyor?")

    # Veriyi gruplayalım
    df_treemap = df.groupby(['neighbourhood_group', 'neighbourhood']).size().reset_index(name='count')
    
    fig_tree = px.treemap(
        df_treemap,
        path=[px.Constant("NYC"), 'neighbourhood_group', 'neighbourhood'],
        values='count',
        color='neighbourhood_group',
        title="Bölge ve Semtlere Göre İlan Yoğunluğu"
    )
    fig_tree.update_traces(hovertemplate='<b>%{label}</b><br>İlan Sayısı: %{value}')
    st.plotly_chart(fig_tree, use_container_width=True)

    st.divider()

    # --- GRAFİK 11: Bölge ve Oda Tipi Kompozisyonu (Stacked Bar Chart) ---
    st.subheader("3. Bölge ve Oda Tipi Kompozisyonu (Stacked Bar)")
    st.info("Soru: Bölgelerin içindeki oda tipi (Özel oda, Evin tamamı vb.) oranları nedir?")

    # Veriyi hazırlama
    df_bar = df.groupby(['neighbourhood_group', 'room_type']).size().reset_index(name='count')

    fig_bar = px.bar(
        df_bar,
        x="neighbourhood_group",
        y="count",
        color="room_type",
        title="Bölgelere Göre Oda Tipi Dağılımı",
        barmode='stack' # Yığınlanmış bar
    )
    fig_bar.update_layout(xaxis_title="Bölge", yaxis_title="İlan Sayısı", legend_title="Oda Tipi")
    st.plotly_chart(fig_bar, use_container_width=True)