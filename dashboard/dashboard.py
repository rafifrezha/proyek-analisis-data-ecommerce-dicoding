import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('dashboard/all_data.csv')
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])

sns.set_palette("Set2")

orders_df = pd.read_csv('data/orders_dataset.csv')
order_items_df = pd.read_csv('data/order_items_dataset.csv')
products_df = pd.read_csv('data/products_dataset.csv')
product_category_df = pd.read_csv('data/product_category_name_translation.csv')

orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])

latest_order_date = orders_df['order_purchase_timestamp'].max()
one_year_ago = latest_order_date - pd.DateOffset(years=1)
three_months_ago = latest_order_date - pd.DateOffset(months=3)

st.title("📊 Dashboard Analisis Pembelian Pelanggan")

tab1, tab2 = st.tabs(["📦 Distribusi Status Pesanan", "💰 Nilai Penjualan per Kategori"])

with tab1:
    st.subheader('Distribusi Status Pesanan Berdasarkan Kategori Produk (Satu Tahun Terakhir)')

    orders_last_year = orders_df[orders_df['order_purchase_timestamp'] >= one_year_ago]

    merged_df = pd.merge(orders_last_year, order_items_df, on='order_id')
    merged_df = pd.merge(merged_df, products_df, on='product_id')
    merged_df = pd.merge(merged_df, product_category_df, how='left', on='product_category_name')

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(data=merged_df, x='product_category_name_english', hue='order_status', palette="Set2", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_title('Distribusi Status Pesanan Berdasarkan Kategori Produk dalam Satu Tahun Terakhir', fontsize=16)
    ax.set_xlabel('Kategori Produk', fontsize=14)
    ax.set_ylabel('Jumlah Pesanan', fontsize=14)
    ax.legend(title='Status Pesanan', loc='upper right')
    plt.tight_layout()
    
    st.pyplot(fig)

with tab2:
    st.subheader('Nilai Penjualan Berdasarkan Kategori Produk (3 Bulan Terakhir)')

    orders_last_3_months = data[data['order_purchase_timestamp'] >= three_months_ago]

    sales_by_category = orders_last_3_months.groupby('product_category_name_english')['price'].sum().reset_index()

    sales_by_category = sales_by_category.sort_values(by='price', ascending=False)

    total_sales_3_months = sales_by_category['price'].sum()

    sales_by_category['contribution_to_total'] = (sales_by_category['price'] / total_sales_3_months) * 100

    fig2, ax2 = plt.subplots(figsize=(12, 8))
    sns.barplot(x='product_category_name_english', y='price', data=sales_by_category, palette="Blues_d", ax=ax2)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    ax2.set_title('Nilai Penjualan Berdasarkan Kategori Produk dalam 3 Bulan Terakhir', fontsize=16)
    ax2.set_xlabel('Kategori Produk', fontsize=14)
    ax2.set_ylabel('Total Penjualan (Rp)', fontsize=14)
    plt.tight_layout()

    st.pyplot(fig2)

    st.markdown(f"**Total Penjualan dalam 3 Bulan Terakhir:** {total_sales_3_months:,.2f}")
    st.markdown(f"**Kategori dengan Penjualan Tertinggi:** {sales_by_category.iloc[0]['product_category_name_english']}")
    st.markdown(f"**Nilai Penjualan Tertinggi:** {sales_by_category.iloc[0]['price']:,.2f}")

    st.markdown("### Top 5 Kategori dengan Penjualan Tertinggi:")
    st.dataframe(sales_by_category.head(5).reset_index(drop=True))
