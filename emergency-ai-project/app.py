import streamlit as st
from sentence_transformers import SentenceTransformer
import json
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

st.title("AI Emergency Resource Locator")

query = st.text_input("Describe your emergency")

with open("dataset.json") as f:
    data = json.load(f)

if query:

    query_embedding = model.encode(query)

    scores = []

    for item in data:

        text = item["name"] + " " + item["service"] + " " + item["location"]

        item_embedding = model.encode(text)

        similarity = np.dot(query_embedding, item_embedding)

        scores.append((similarity, item))

    scores.sort(reverse=True)

    st.subheader("Recommended Emergency Services")

    for score,item in scores[:3]:

        st.write("Name:",item["name"])
        st.write("Type:",item["type"])
        st.write("Location:",item["location"])
        st.write("Service:",item["service"])
        st.write("---")
