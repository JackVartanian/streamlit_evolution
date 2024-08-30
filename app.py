import streamlit as st
import pandas as pd
import numpy as np
import requests

import base64
from PIL import Image
from io import BytesIO

headers_v1 = {"apikey": "ari9fwCNAdhu8YRlq9nZbWvtNU3hW1lP"}
headers_v2 = {"apikey": "V24TSZWSTASDADSADSADSKHYD3"}


def consultInstance_v1():

    url = "https://chatwoot-evolutionapi.oxntyx.easypanel.host/instance/fetchInstances"
    querystring = {"instanceName": option}
    response = requests.request("GET", url, headers=headers_v1, params=querystring)
    return response.json()["instance"]["status"]


def connectInstance_v1(option):

    url = (
        "https://chatwoot-evolutionapi.oxntyx.easypanel.host/instance/connect/" + option
    )
    response = requests.request("GET", url, headers=headers_v1)
    return response.json().get("base64", "")


def consultInstance_v2():

    url = "https://listmonk-evolution2.oxntyx.easypanel.host/instance/fetchInstances"
    querystring = {"instanceName": option}
    headers = {"apikey": "V24TSZWSTASDADSADSADSKHYD3"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()[0]["connectionStatus"]


def connectInstance_v2(option):
    url = "https://listmonk-evolution2.oxntyx.easypanel.host/instance/connect/" + option
    headers = {"apikey": "V24TSZWSTASDADSADSADSKHYD3"}
    response = requests.request("GET", url, headers=headers)
    return response.json().get("base64", "")


def convertBase64(base64_string):
    if not base64_string:
        st.error("A resposta não contém uma string base64 válida.")
    else:
        base64_string = (
            base64_string.split(",")[1] if "," in base64_string else base64_string
        )

    base64_string += "=" * ((4 - len(base64_string) % 4) % 4)

    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        st.image(image)
        st.caption("Leia esse :red[QR Code] :smile:")
    except Exception as e:
        st.error(f"Erro ao decodificar a imagem: {e}")


def showQrcode_v2():
    if consultInstance_v2() == "open":
        st.header("Conectado")
    else:
        st.warning("Não conectado!")
        base64_string = connectInstance_v2(option)
        convertBase64(base64_string)


def showQrcode_v1():
    if consultInstance_v1() != "open":
        st.markdown("Abra seu WhatsApp e escaneie o QR Code.")
        base64_string = connectInstance_v1(option)
        convertBase64(base64_string)
        if st.button("Clique para atualizar"):
            st.caching.clear_cache()
            st.experimental_rerun()


col1, col2 = st.columns(2)
with col1:
    option = st.selectbox(
        "Selecione uma opção",
        (
            "Aline",
            "Giovanna",
            "Giovani",
            "Lorena",
            "Poliane",
            "Simara",
            "Vanessa",
            "Jean",
            "Teste",
        ),
    )

with col2:
    if consultInstance_v1() == "open":
        st.header("Conectado")
        st.balloons()
    else:
        st.text("")
        st.error("Não conectado!")

showQrcode_v1()
