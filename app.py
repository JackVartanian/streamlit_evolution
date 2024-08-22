import streamlit as st
import pandas as pd
import numpy as np
import requests

import base64
from PIL import Image
from io import BytesIO

option = st.selectbox(
    "Selecione uma opção",
    ("Aline", "Giovanna", "Giovani", "Lorena", "Poliane", "Simara", "Vanessa", "Jean"),
)


# url = "https://listmonk-evolution2.oxntyx.easypanel.host/instance/connect/" + option
# headers = {"apikey": "V24TSZWSTASDADSADSADSKHYD3"}
# querystring = {"number": "5511989927965"}

# # response = requests.request("GET", url, headers=headers)
# response = requests.request("GET", url, headers=headers, params=querystring)

# st.text(response.json())


def consultInstance():

    url = "https://listmonk-evolution2.oxntyx.easypanel.host/instance/fetchInstances"
    querystring = {"instanceName": option}
    headers = {"apikey": "V24TSZWSTASDADSADSADSKHYD3"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()[0]["connectionStatus"]


def connectInstance(option):
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
        st.image(image, caption="Imagem decodificada")
    except Exception as e:
        st.error(f"Erro ao decodificar a imagem: {e}")


def showQrcode():
    if consultInstance() == "open":
        st.header("Conectado")
    else:
        st.warning("Não conectado!")
        base64_string = connectInstance(option)
        convertBase64(base64_string)


showQrcode()
