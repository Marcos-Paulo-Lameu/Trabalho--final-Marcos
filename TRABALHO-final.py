import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def raspar_terabyte():
    url = 'https://www.terabyteshop.com.br'
    endpoint = '/hardware/placas-de-video'
    url_completa = url + endpoint
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url_completa)
    time.sleep(2)
    
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    produtos = []
    for produto in soup.find_all('div', class_='box-product'):
        nome = produto.find('h2', class_='name').get_text(strip=True)
        preco = produto.find('span', class_='price-new').get_text(strip=True)
        produtos.append({'Nome': nome, 'Preço': preco})
    
    return produtos

lista_produtos = raspar_terabyte()

if lista_produtos:
    print("Produtos de Placas de Vídeo na TerabyteShop:")
    for produto in lista_produtos[:5]:
        print(f"{produto['Nome']} - Preço: {produto['Preço']}")
else:
    print("Não foi possível obter os produtos da TerabyteShop.")

df_produtos = pd.DataFrame(lista_produtos)

print("\nInformações básicas sobre os dados:")
print(df_produtos.info())

print("\nEstatísticas descritivas dos preços:")
print(df_produtos['Preço'].describe())

plt.figure(figsize=(10, 6))
plt.bar(df_produtos['Nome'][:10], df_produtos['Preço'][:10], color='skyblue')
plt.title('Top 10 Placas de Vídeo - Preços')
plt.xlabel('Nome do Produto')
plt.ylabel('Preço (R$)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

st.title('Produtos de Placas de Vídeo na TerabyteShop')
st.write(df_produtos)

def gerar_pdf(produtos):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 750, "Produtos de Placas de Vídeo na TerabyteShop")
    
    pdf.setFont("Helvetica", 12)
    y = 700
    for idx, produto in produtos.iterrows():
        y -= 20
        pdf.drawString(100, y, f"Produto: {produto['Nome']} - Preço: {produto['Preço']}")
    
    pdf.save()
    buffer.seek(0)
    
    return buffer

pdf_buffer = gerar_pdf(df_produtos)
st.markdown("### Exportar para PDF")
st.markdown("Clique [aqui](data:application/pdf;base64,{}) para baixar o PDF.".format(
    pdf_buffer.getvalue().encode("base64").decode()
))
