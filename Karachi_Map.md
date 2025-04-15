```py
import random
import streamlit as st
from queue import PriorityQueue
import matplotlib.pyplot as plt
import math
from collections import defaultdict

st.set_page_config(page_title="Karachi Market Path Finder", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }

    .stApp {
        background-color: #f0f2f6;
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }

    .stSelectbox > label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }

    .stSelectbox .css-1wa3eu0-placeholder {
        color: #999;
    }

    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }

    .stButton>button {
        width: 60%;
        background-color: #3498db;
        color: white;
        padding: 0.85rem 1.5rem;
        border: none;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }

    .stButton>button:hover {
        background-color: #2980b9;
    }

    .block-container {
        padding: 2rem 3rem;
    }

    .result-container {
        background-color: #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        margin-top: 1.5rem;
        color: #2c3e50;
        font-size: 1.05rem;
    }

    .path-highlight {
        color: #3498db;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Area coordinates
area_coords = {
    'Clifton': [24.8138, 67.0304],
    'Saddar': [24.8540, 67.0301],
    'Lyari': [24.8722, 66.9999],
    'Korangi': [24.8296, 67.1302],
    'Landhi': [24.8500, 67.2000],
    'Malir': [24.8934, 67.2066],
    'Gulshan-e-Iqbal': [24.9180, 67.1120],
    'Gulistan-e-Johar': [24.9300, 67.1400],
    'North Nazimabad': [24.9500, 67.0364],
    'Nazimabad': [24.9200, 67.0300],
    'Federal B Area': [24.9300, 67.0700],
    'PECHS': [24.8700, 67.0700],
    'Shah Faisal Colony': [24.8700, 67.1600],
    'Model Colony': [24.9000, 67.1800],
    'Defence Phase 1': [24.7870, 67.0330],
    'Defence Phase 2': [24.7980, 67.0450],
    'Defence Phase 5': [24.8070, 67.0620],
    'Defence Phase 8': [24.8145, 67.0815],
    'Mehmoodabad': [24.8660, 67.0820],
    'Manzoor Colony': [24.8645, 67.0768],
    'Liaquatabad': [24.9135, 67.0500],
    'Ancholi': [24.9392, 67.0784],
    'Nagan Chowrangi': [24.9591, 67.0642],
    'Sohrab Goth': [24.9735, 67.1033],
    'New Karachi': [24.9750, 67.0670],
    'Shadman Town': [24.9700, 67.0300],
    'North Karachi': [24.9705, 67.0588],
    'Surjani Town': [25.0022, 67.0289],
    'Orangi Town': [24.9500, 66.9900],
    'Baldia Town': [24.9360, 66.9610],
    'Kemari': [24.8422, 66.9730],
    'Hawksbay': [24.8290, 66.9040],
    'Sea View': [24.7933, 67.0642],
    'Gizri': [24.8031, 67.0463],
    'Kharadar': [24.8520, 67.0018],
    'Garden East': [24.8730, 67.0375],
    'Garden West': [24.8700, 67.0300],
    'Jacob Lines': [24.8665, 67.0437],
    'Soldier Bazaar': [24.8643, 67.0342],
    'Lines Area': [24.8600, 67.0415]
}

# Graph representation
graph = {
    'Clifton': [('Saddar', 49), ('Lyari', 18), ('Korangi', 31), ('Landhi', 15), ('Malir', 7), ('Gulshan-e-Iqbal', 42), ('Gulistan-e-Johar', 21), ('North Nazimabad', 48), ('Nazimabad', 42), ('Federal B Area', 33), ('PECHS', 17), ('Shah Faisal Colony', 17), ('Model Colony', 6), ('Defence Phase 1', 42), ('Defence Phase 2', 10), ('Defence Phase 5', 49), ('Defence Phase 8', 29), ('Mehmoodabad', 22), ('Manzoor Colony', 37), ('Liaquatabad', 10), ('Ancholi', 28), ('Nagan Chowrangi', 27), ('Sohrab Goth', 42), ('New Karachi', 17), ('Shadman Town', 28), ('North Karachi', 19), ('Surjani Town', 7), ('Orangi Town', 49), ('Baldia Town', 37), ('Kemari', 18), ('Hawksbay', 22), ('Sea View', 43), ('Gizri', 36), ('Kharadar', 46), ('Garden East', 47), ('Garden West', 21), ('Jacob Lines', 7), ('Soldier Bazaar', 37), ('Lines Area', 34)],
    'Saddar': [('Clifton', 24), ('Lyari', 44), ('Korangi', 30), ('Landhi', 18), ('Malir', 18), ('Gulshan-e-Iqbal', 13), ('Gulistan-e-Johar', 11), ('North Nazimabad', 12), ('Nazimabad', 14), ('Federal B Area', 45), ('PECHS', 26), ('Shah Faisal Colony', 17), ('Model Colony', 39), ('Defence Phase 1', 45), ('Defence Phase 2', 32), ('Defence Phase 5', 12), ('Defence Phase 8', 18), ('Mehmoodabad', 13), ('Manzoor Colony', 27), ('Liaquatabad', 19), ('Ancholi', 23), ('Nagan Chowrangi', 45), ('Sohrab Goth', 25), ('New Karachi', 6), ('Shadman Town', 33), ('North Karachi', 15), ('Surjani Town', 37), ('Orangi Town', 22), ('Baldia Town', 25), ('Kemari', 30), ('Hawksbay', 7), ('Sea View', 25), ('Gizri', 29), ('Kharadar', 43), ('Garden East', 20), ('Garden West', 36), ('Jacob Lines', 45), ('Soldier Bazaar', 21), ('Lines Area', 16)],
    'Lyari': [('Clifton', 20), ('Saddar', 7), ('Korangi', 25), ('Landhi', 22), ('Malir', 33), ('Gulshan-e-Iqbal', 43), ('Gulistan-e-Johar', 9), ('North Nazimabad', 27), ('Nazimabad', 31), ('Federal B Area', 34), ('PECHS', 50), ('Shah Faisal Colony', 14), ('Model Colony', 12), ('Defence Phase 1', 34), ('Defence Phase 2', 32), ('Defence Phase 5', 40), ('Defence Phase 8', 26), ('Mehmoodabad', 18), ('Manzoor Colony', 46), ('Liaquatabad', 21), ('Ancholi', 27), ('Nagan Chowrangi', 13), ('Sohrab Goth', 41), ('New Karachi', 28), ('Shadman Town', 20), ('North Karachi', 35), ('Surjani Town', 6), ('Orangi Town', 16), ('Baldia Town', 30), ('Kemari', 44), ('Hawksbay', 44), ('Sea View', 38), ('Gizri', 35), ('Kharadar', 12), ('Garden East', 8), ('Garden West', 23), ('Jacob Lines', 22), ('Soldier Bazaar', 35), ('Lines Area', 49)],
    'Korangi': [('Clifton', 39), ('Saddar', 20), ('Lyari', 18), ('Landhi', 10), ('Malir', 22), ('Gulshan-e-Iqbal', 29), ('Gulistan-e-Johar', 33), ('North Nazimabad', 13), ('Nazimabad', 10), ('Federal B Area', 36), ('PECHS', 31), ('Shah Faisal Colony', 42), ('Model Colony', 13), ('Defence Phase 1', 20), ('Defence Phase 2', 15), ('Defence Phase 5', 7), ('Defence Phase 8', 18), ('Mehmoodabad', 10), ('Manzoor Colony', 17), ('Liaquatabad', 17), ('Ancholi', 18), ('Nagan Chowrangi', 42), ('Sohrab Goth', 34), ('New Karachi', 34), ('Shadman Town', 40), ('North Karachi', 11), ('Surjani Town', 9), ('Orangi Town', 14), ('Baldia Town', 26), ('Kemari', 21), ('Hawksbay', 18), ('Sea View', 15), ('Gizri', 34), ('Kharadar', 13), ('Garden East', 24), ('Garden West', 10), ('Jacob Lines', 27), ('Soldier Bazaar', 26), ('Lines Area', 10)],
    'Landhi': [('Clifton', 32), ('Saddar', 31), ('Lyari', 38), ('Korangi', 25), ('Malir', 18), ('Gulshan-e-Iqbal', 40), ('Gulistan-e-Johar', 15), ('North Nazimabad', 6), ('Nazimabad', 40), ('Federal B Area', 28), ('PECHS', 12), ('Shah Faisal Colony', 18), ('Model Colony', 50), ('Defence Phase 1', 8), ('Defence Phase 2', 37), ('Defence Phase 5', 7), ('Defence Phase 8', 34), ('Mehmoodabad', 40), ('Manzoor Colony', 45), ('Liaquatabad', 34), ('Ancholi', 42), ('Nagan Chowrangi', 44), ('Sohrab Goth', 40), ('New Karachi', 16), ('Shadman Town', 15), ('North Karachi', 34), ('Surjani Town', 15), ('Orangi Town', 27), ('Baldia Town', 39), ('Kemari', 49), ('Hawksbay', 42), ('Sea View', 13), ('Gizri', 18), ('Kharadar', 12), ('Garden East', 22), ('Garden West', 43), ('Jacob Lines', 23), ('Soldier Bazaar', 18), ('Lines Area', 43)],
    'Malir': [('Clifton', 22), ('Saddar', 14), ('Lyari', 27), ('Korangi', 32), ('Landhi', 7), ('Gulshan-e-Iqbal', 33), ('Gulistan-e-Johar', 24), ('North Nazimabad', 37), ('Nazimabad', 29), ('Federal B Area', 22), ('PECHS', 47), ('Shah Faisal Colony', 9), ('Model Colony', 16), ('Defence Phase 1', 11), ('Defence Phase 2', 41), ('Defence Phase 5', 34), ('Defence Phase 8', 39), ('Mehmoodabad', 13), ('Manzoor Colony', 39), ('Liaquatabad', 45), ('Ancholi', 24), ('Nagan Chowrangi', 48), ('Sohrab Goth', 21), ('New Karachi', 30), ('Shadman Town', 45), ('North Karachi', 21), ('Surjani Town', 34), ('Orangi Town', 28), ('Baldia Town', 37), ('Kemari', 43), ('Hawksbay', 45), ('Sea View', 20), ('Gizri', 22), ('Kharadar', 18), ('Garden East', 44), ('Garden West', 49), ('Jacob Lines', 27), ('Soldier Bazaar', 9), ('Lines Area', 5)],
    'Gulshan-e-Iqbal': [('Clifton', 50), ('Saddar', 19), ('Lyari', 23), ('Korangi', 43), ('Landhi', 29), ('Malir', 41), ('Gulistan-e-Johar', 7), ('North Nazimabad', 49), ('Nazimabad', 27), ('Federal B Area', 12), ('PECHS', 15), ('Shah Faisal Colony', 46), ('Model Colony', 46), ('Defence Phase 1', 38), ('Defence Phase 2', 22), ('Defence Phase 5', 20), ('Defence Phase 8', 9), ('Mehmoodabad', 46), ('Manzoor Colony', 41), ('Liaquatabad', 12), ('Ancholi', 10), ('Nagan Chowrangi', 31), ('Sohrab Goth', 38), ('New Karachi', 14), ('Shadman Town', 25), ('North Karachi', 13), ('Surjani Town', 45), ('Orangi Town', 38), ('Baldia Town', 26), ('Kemari', 19), ('Hawksbay', 34), ('Sea View', 7), ('Gizri', 14), ('Kharadar', 23), ('Garden East', 50), ('Garden West', 11), ('Jacob Lines', 36), ('Soldier Bazaar', 36), ('Lines Area', 19)],
    'Gulistan-e-Johar': [('Clifton', 43), ('Saddar', 22), ('Lyari', 19), ('Korangi', 48), ('Landhi', 40), ('Malir', 30), ('Gulshan-e-Iqbal', 40), ('North Nazimabad', 16), ('Nazimabad', 15), ('Federal B Area', 29), ('PECHS', 12), ('Shah Faisal Colony', 22), ('Model Colony', 40), ('Defence Phase 1', 9), ('Defence Phase 2', 39), ('Defence Phase 5', 24), ('Defence Phase 8', 26), ('Mehmoodabad', 41), ('Manzoor Colony', 34), ('Liaquatabad', 35), ('Ancholi', 16), ('Nagan Chowrangi', 35), ('Sohrab Goth', 28), ('New Karachi', 6), ('Shadman Town', 34), ('North Karachi', 6), ('Surjani Town', 29), ('Orangi Town', 39), ('Baldia Town', 5), ('Kemari', 43), ('Hawksbay', 41), ('Sea View', 43), ('Gizri', 21), ('Kharadar', 25), ('Garden East', 6), ('Garden West', 10), ('Jacob Lines', 25), ('Soldier Bazaar', 21), ('Lines Area', 50)],
    'North Nazimabad': [('Clifton', 10), ('Saddar', 42), ('Lyari', 28), ('Korangi', 48), ('Landhi', 18), ('Malir', 50), ('Gulshan-e-Iqbal', 20), ('Gulistan-e-Johar', 19), ('Nazimabad', 28), ('Federal B Area', 23), ('PECHS', 17), ('Shah Faisal Colony', 10), ('Model Colony', 19), ('Defence Phase 1', 45), ('Defence Phase 2', 33), ('Defence Phase 5', 17), ('Defence Phase 8', 36), ('Mehmoodabad', 9), ('Manzoor Colony', 20), ('Liaquatabad', 38), ('Ancholi', 8), ('Nagan Chowrangi', 7), ('Sohrab Goth', 16), ('New Karachi', 20), ('Shadman Town', 8), ('North Karachi', 28), ('Surjani Town', 21), ('Orangi Town', 21), ('Baldia Town', 25), ('Kemari', 33), ('Hawksbay', 42), ('Sea View', 42), ('Gizri', 7), ('Kharadar', 48), ('Garden East', 14), ('Garden West', 14), ('Jacob Lines', 35), ('Soldier Bazaar', 15), ('Lines Area', 35)],
    'Nazimabad': [('Clifton', 38), ('Saddar', 50), ('Lyari', 41), ('Korangi', 12), ('Landhi', 21), ('Malir', 18), ('Gulshan-e-Iqbal', 21), ('Gulistan-e-Johar', 13), ('North Nazimabad', 14), ('Federal B Area', 32), ('PECHS', 12), ('Shah Faisal Colony', 5), ('Model Colony', 32), ('Defence Phase 1', 46), ('Defence Phase 2', 6), ('Defence Phase 5', 31), ('Defence Phase 8', 48), ('Mehmoodabad', 16), ('Manzoor Colony', 26), ('Liaquatabad', 22), ('Ancholi', 36), ('Nagan Chowrangi', 24), ('Sohrab Goth', 19), ('New Karachi', 47), ('Shadman Town', 10), ('North Karachi', 34), ('Surjani Town', 30), ('Orangi Town', 39), ('Baldia Town', 38), ('Kemari', 7), ('Hawksbay', 29), ('Sea View', 44), ('Gizri', 41), ('Kharadar', 37), ('Garden East', 13), ('Garden West', 49), ('Jacob Lines', 17), ('Soldier Bazaar', 20), ('Lines Area', 40)],
    'Federal B Area': [('Clifton', 11), ('Saddar', 47), ('Lyari', 39), ('Korangi', 40), ('Landhi', 42), ('Malir', 27), ('Gulshan-e-Iqbal', 48), ('Gulistan-e-Johar', 20), ('North Nazimabad', 18), ('Nazimabad', 23), ('PECHS', 37), ('Shah Faisal Colony', 37), ('Model Colony', 11), ('Defence Phase 1', 22), ('Defence Phase 2', 30), ('Defence Phase 5', 24), ('Defence Phase 8', 32), ('Mehmoodabad', 46), ('Manzoor Colony', 23), ('Liaquatabad', 41), ('Ancholi', 9), ('Nagan Chowrangi', 40), ('Sohrab Goth', 40), ('New Karachi', 11), ('Shadman Town', 17), ('North Karachi', 30), ('Surjani Town', 42), ('Orangi Town', 46), ('Baldia Town', 42), ('Kemari', 15), ('Hawksbay', 18), ('Sea View', 31), ('Gizri', 30), ('Kharadar', 16), ('Garden East', 23), ('Garden West', 27), ('Jacob Lines', 19), ('Soldier Bazaar', 28), ('Lines Area', 38)],
    'PECHS': [('Clifton', 41), ('Saddar', 37), ('Lyari', 15), ('Korangi', 15), ('Landhi', 28), ('Malir', 36), ('Gulshan-e-Iqbal', 29), ('Gulistan-e-Johar', 15), ('North Nazimabad', 38), ('Nazimabad', 36), ('Federal B Area', 14), ('Shah Faisal Colony', 17), ('Model Colony', 5), ('Defence Phase 1', 12), ('Defence Phase 2', 23), ('Defence Phase 5', 42), ('Defence Phase 8', 45), ('Mehmoodabad', 46), ('Manzoor Colony', 49), ('Liaquatabad', 9), ('Ancholi', 26), ('Nagan Chowrangi', 13), ('Sohrab Goth', 25), ('New Karachi', 5), ('Shadman Town', 43), ('North Karachi', 41), ('Surjani Town', 48), ('Orangi Town', 45), ('Baldia Town', 39), ('Kemari', 9), ('Hawksbay', 42), ('Sea View', 23), ('Gizri', 34), ('Kharadar', 45), ('Garden East', 13), ('Garden West', 44), ('Jacob Lines', 24), ('Soldier Bazaar', 47), ('Lines Area', 7)],
    'Shah Faisal Colony': [('Clifton', 42), ('Saddar', 50), ('Lyari', 24), ('Korangi', 24), ('Landhi', 38), ('Malir', 42), ('Gulshan-e-Iqbal', 44), ('Gulistan-e-Johar', 31), ('North Nazimabad', 37), ('Nazimabad', 10), ('Federal B Area', 42), ('PECHS', 46), ('Model Colony', 42), ('Defence Phase 1', 37), ('Defence Phase 2', 40), ('Defence Phase 5', 15), ('Defence Phase 8', 13), ('Mehmoodabad', 8), ('Manzoor Colony', 32), ('Liaquatabad', 35), ('Ancholi', 19), ('Nagan Chowrangi', 49), ('Sohrab Goth', 25), ('New Karachi', 16), ('Shadman Town', 48), ('North Karachi', 6), ('Surjani Town', 24), ('Orangi Town', 5), ('Baldia Town', 38), ('Kemari', 46), ('Hawksbay', 50), ('Sea View', 46), ('Gizri', 27), ('Kharadar', 46), ('Garden East', 32), ('Garden West', 9), ('Jacob Lines', 49), ('Soldier Bazaar', 27), ('Lines Area', 39)],
    'Model Colony': [('Clifton', 38), ('Saddar', 43), ('Lyari', 44), ('Korangi', 49), ('Landhi', 23), ('Malir', 21), ('Gulshan-e-Iqbal', 42), ('Gulistan-e-Johar', 43), ('North Nazimabad', 34), ('Nazimabad', 36), ('Federal B Area', 9), ('PECHS', 20), ('Shah Faisal Colony', 23), ('Defence Phase 1', 13), ('Defence Phase 2', 38), ('Defence Phase 5', 47), ('Defence Phase 8', 26), ('Mehmoodabad', 49), ('Manzoor Colony', 37), ('Liaquatabad', 39), ('Ancholi', 27), ('Nagan Chowrangi', 24), ('Sohrab Goth', 34), ('New Karachi', 40), ('Shadman Town', 47), ('North Karachi', 31), ('Surjani Town', 43), ('Orangi Town', 13), ('Baldia Town', 49), ('Kemari', 22), ('Hawksbay', 29), ('Sea View', 42), ('Gizri', 22), ('Kharadar', 39), ('Garden East', 24), ('Garden West', 46), ('Jacob Lines', 16), ('Soldier Bazaar', 8), ('Lines Area', 37)],
    'Defence Phase 1': [('Clifton', 9), ('Saddar', 7), ('Lyari', 20), ('Korangi', 23), ('Landhi', 41), ('Malir', 31), ('Gulshan-e-Iqbal', 36), ('Gulistan-e-Johar', 6), ('North Nazimabad', 33), ('Nazimabad', 27), ('Federal B Area', 16), ('PECHS', 19), ('Shah Faisal Colony', 12), ('Model Colony', 39), ('Defence Phase 2', 44), ('Defence Phase 5', 46), ('Defence Phase 8', 35), ('Mehmoodabad', 49), ('Manzoor Colony', 39), ('Liaquatabad', 20), ('Ancholi', 39), ('Nagan Chowrangi', 27), ('Sohrab Goth', 9), ('New Karachi', 13), ('Shadman Town', 28), ('North Karachi', 43), ('Surjani Town', 31), ('Orangi Town', 45), ('Baldia Town', 36), ('Kemari', 15), ('Hawksbay', 42), ('Sea View', 8), ('Gizri', 11), ('Kharadar', 6), ('Garden East', 14), ('Garden West', 24), ('Jacob Lines', 48), ('Soldier Bazaar', 17), ('Lines Area', 47)],
    'Defence Phase 2': [('Clifton', 39), ('Saddar', 30), ('Lyari', 41), ('Korangi', 48), ('Landhi', 7), ('Malir', 21), ('Gulshan-e-Iqbal', 28), ('Gulistan-e-Johar', 20), ('North Nazimabad', 47), ('Nazimabad', 32), ('Federal B Area', 24), ('PECHS', 29), ('Shah Faisal Colony', 20), ('Model Colony', 15), ('Defence Phase 1', 26), ('Defence Phase 5', 21), ('Defence Phase 8', 18), ('Mehmoodabad', 25), ('Manzoor Colony', 20), ('Liaquatabad', 27), ('Ancholi', 41), ('Nagan Chowrangi', 37), ('Sohrab Goth', 16), ('New Karachi', 48), ('Shadman Town', 8), ('North Karachi', 43), ('Surjani Town', 35), ('Orangi Town', 11), ('Baldia Town', 40), ('Kemari', 39), ('Hawksbay', 23), ('Sea View', 36), ('Gizri', 10), ('Kharadar', 30), ('Garden East', 30), ('Garden West', 21), ('Jacob Lines', 46), ('Soldier Bazaar', 29), ('Lines Area', 5)],
    'Defence Phase 5': [('Clifton', 21), ('Saddar', 9), ('Lyari', 36), ('Korangi', 15), ('Landhi', 28), ('Malir', 16), ('Gulshan-e-Iqbal', 21), ('Gulistan-e-Johar', 43), ('North Nazimabad', 47), ('Nazimabad', 8), ('Federal B Area', 27), ('PECHS', 10), ('Shah Faisal Colony', 18), ('Model Colony', 31), ('Defence Phase 1', 16), ('Defence Phase 2', 32), ('Defence Phase 8', 7), ('Mehmoodabad', 15), ('Manzoor Colony', 24), ('Liaquatabad', 26), ('Ancholi', 47), ('Nagan Chowrangi', 43), ('Sohrab Goth', 10), ('New Karachi', 45), ('Shadman Town', 37), ('North Karachi', 29), ('Surjani Town', 45), ('Orangi Town', 7), ('Baldia Town', 45), ('Kemari', 27), ('Hawksbay', 35), ('Sea View', 15), ('Gizri', 27), ('Kharadar', 9), ('Garden East', 45), ('Garden West', 24), ('Jacob Lines', 40), ('Soldier Bazaar', 21), ('Lines Area', 12)],
    'Defence Phase 8': [('Clifton', 37), ('Saddar', 9), ('Lyari', 6), ('Korangi', 37), ('Landhi', 43), ('Malir', 34), ('Gulshan-e-Iqbal', 28), ('Gulistan-e-Johar', 25), ('North Nazimabad', 16), ('Nazimabad', 28), ('Federal B Area', 38), ('PECHS', 21), ('Shah Faisal Colony', 33), ('Model Colony', 18), ('Defence Phase 1', 41), ('Defence Phase 2', 17), ('Defence Phase 5', 11), ('Mehmoodabad', 15), ('Manzoor Colony', 27), ('Liaquatabad', 26), ('Ancholi', 20), ('Nagan Chowrangi', 9), ('Sohrab Goth', 46), ('New Karachi', 29), ('Shadman Town', 43), ('North Karachi', 18), ('Surjani Town', 29), ('Orangi Town', 23), ('Baldia Town', 10), ('Kemari', 20), ('Hawksbay', 22), ('Sea View', 18), ('Gizri', 12), ('Kharadar', 38), ('Garden East', 50), ('Garden West', 49), ('Jacob Lines', 45), ('Soldier Bazaar', 39), ('Lines Area', 33)],
    'Mehmoodabad': [('Clifton', 6), ('Saddar', 35), ('Lyari', 39), ('Korangi', 15), ('Landhi', 46), ('Malir', 17), ('Gulshan-e-Iqbal', 28), ('Gulistan-e-Johar', 36), ('North Nazimabad', 46), ('Nazimabad', 9), ('Federal B Area', 41), ('PECHS', 25), ('Shah Faisal Colony', 26), ('Model Colony', 23), ('Defence Phase 1', 5), ('Defence Phase 2', 7), ('Defence Phase 5', 11), ('Defence Phase 8', 29), ('Manzoor Colony', 30), ('Liaquatabad', 8), ('Ancholi', 27), ('Nagan Chowrangi', 36), ('Sohrab Goth', 16), ('New Karachi', 28), ('Shadman Town', 23), ('North Karachi', 48), ('Surjani Town', 40), ('Orangi Town', 17), ('Baldia Town', 27), ('Kemari', 13), ('Hawksbay', 12), ('Sea View', 31), ('Gizri', 23), ('Kharadar', 11), ('Garden East', 29), ('Garden West', 37), ('Jacob Lines', 8), ('Soldier Bazaar', 17), ('Lines Area', 12)],
    'Manzoor Colony': [('Clifton', 25), ('Saddar', 33), ('Lyari', 32), ('Korangi', 5), ('Landhi', 18), ('Malir', 43), ('Gulshan-e-Iqbal', 29), ('Gulistan-e-Johar', 24), ('North Nazimabad', 5), ('Nazimabad', 12), ('Federal B Area', 24), ('PECHS', 46), ('Shah Faisal Colony', 41), ('Model Colony', 45), ('Defence Phase 1', 37), ('Defence Phase 2', 49), ('Defence Phase 5', 46), ('Defence Phase 8', 25), ('Mehmoodabad', 23), ('Liaquatabad', 32), ('Ancholi', 32), ('Nagan Chowrangi', 47), ('Sohrab Goth', 8), ('New Karachi', 38), ('Shadman Town', 7), ('North Karachi', 24), ('Surjani Town', 32), ('Orangi Town', 30), ('Baldia Town', 50), ('Kemari', 50), ('Hawksbay', 10), ('Sea View', 17), ('Gizri', 50), ('Kharadar', 34), ('Garden East', 37), ('Garden West', 33), ('Jacob Lines', 50), ('Soldier Bazaar', 38), ('Lines Area', 44)],
    'Liaquatabad': [('Clifton', 11), ('Saddar', 46), ('Lyari', 46), ('Korangi', 19), ('Landhi', 32), ('Malir', 44), ('Gulshan-e-Iqbal', 23), ('Gulistan-e-Johar', 12), ('North Nazimabad', 22), ('Nazimabad', 50), ('Federal B Area', 21), ('PECHS', 40), ('Shah Faisal Colony', 32), ('Model Colony', 6), ('Defence Phase 1', 25), ('Defence Phase 2', 7), ('Defence Phase 5', 22), ('Defence Phase 8', 16), ('Mehmoodabad', 42), ('Manzoor Colony', 9), ('Ancholi', 17), ('Nagan Chowrangi', 20), ('Sohrab Goth', 9), ('New Karachi', 10), ('Shadman Town', 40), ('North Karachi', 31), ('Surjani Town', 35), ('Orangi Town', 14), ('Baldia Town', 49), ('Kemari', 6), ('Hawksbay', 35), ('Sea View', 16), ('Gizri', 25), ('Kharadar', 42), ('Garden East', 32), ('Garden West', 42), ('Jacob Lines', 39), ('Soldier Bazaar', 22), ('Lines Area', 39)],
    'Ancholi': [('Clifton', 15), ('Saddar', 11), ('Lyari', 30), ('Korangi', 23), ('Landhi', 26), ('Malir', 22), ('Gulshan-e-Iqbal', 5), ('Gulistan-e-Johar', 35), ('North Nazimabad', 21), ('Nazimabad', 11), ('Federal B Area', 19), ('PECHS', 37), ('Shah Faisal Colony', 14), ('Model Colony', 17), ('Defence Phase 1', 31), ('Defence Phase 2', 7), ('Defence Phase 5', 46), ('Defence Phase 8', 31), ('Mehmoodabad', 40), ('Manzoor Colony', 49), ('Liaquatabad', 42), ('Nagan Chowrangi', 41), ('Sohrab Goth', 28), ('New Karachi', 9), ('Shadman Town', 45), ('North Karachi', 19), ('Surjani Town', 28), ('Orangi Town', 49), ('Baldia Town', 16), ('Kemari', 45), ('Hawksbay', 43), ('Sea View', 24), ('Gizri', 18), ('Kharadar', 8), ('Garden East', 24), ('Garden West', 18), ('Jacob Lines', 50), ('Soldier Bazaar', 23), ('Lines Area', 49)],
    'Nagan Chowrangi': [('Clifton', 11), ('Saddar', 27), ('Lyari', 18), ('Korangi', 39), ('Landhi', 48), ('Malir', 39), ('Gulshan-e-Iqbal', 18), ('Gulistan-e-Johar', 42), ('North Nazimabad', 34), ('Nazimabad', 30), ('Federal B Area', 7), ('PECHS', 26), ('Shah Faisal Colony', 16), ('Model Colony', 6), ('Defence Phase 1', 29), ('Defence Phase 2', 31), ('Defence Phase 5', 34), ('Defence Phase 8', 9), ('Mehmoodabad', 16), ('Manzoor Colony', 28), ('Liaquatabad', 46), ('Ancholi', 24), ('Sohrab Goth', 40), ('New Karachi', 46), ('Shadman Town', 10), ('North Karachi', 37), ('Surjani Town', 31), ('Orangi Town', 40), ('Baldia Town', 7), ('Kemari', 22), ('Hawksbay', 47), ('Sea View', 33), ('Gizri', 13), ('Kharadar', 12), ('Garden East', 38), ('Garden West', 18), ('Jacob Lines', 14), ('Soldier Bazaar', 27), ('Lines Area', 37)],
    'Sohrab Goth': [('Clifton', 50), ('Saddar', 45), ('Lyari', 19), ('Korangi', 21), ('Landhi', 25), ('Malir', 14), ('Gulshan-e-Iqbal', 46), ('Gulistan-e-Johar', 36), ('North Nazimabad', 13), ('Nazimabad', 8), ('Federal B Area', 39), ('PECHS', 36), ('Shah Faisal Colony', 27), ('Model Colony', 26), ('Defence Phase 1', 36), ('Defence Phase 2', 38), ('Defence Phase 5', 5), ('Defence Phase 8', 23), ('Mehmoodabad', 47), ('Manzoor Colony', 32), ('Liaquatabad', 30), ('Ancholi', 38), ('Nagan Chowrangi', 27), ('New Karachi', 39), ('Shadman Town', 5), ('North Karachi', 46), ('Surjani Town', 34), ('Orangi Town', 38), ('Baldia Town', 37), ('Kemari', 7), ('Hawksbay', 10), ('Sea View', 33), ('Gizri', 34), ('Kharadar', 16), ('Garden East', 13), ('Garden West', 36), ('Jacob Lines', 13), ('Soldier Bazaar', 8), ('Lines Area', 28)],
    'New Karachi': [('Clifton', 32), ('Saddar', 30), ('Lyari', 21), ('Korangi', 42), ('Landhi', 39), ('Malir', 13), ('Gulshan-e-Iqbal', 42), ('Gulistan-e-Johar', 50), ('North Nazimabad', 26), ('Nazimabad', 15), ('Federal B Area', 43), ('PECHS', 17), ('Shah Faisal Colony', 43), ('Model Colony', 14), ('Defence Phase 1', 38), ('Defence Phase 2', 9), ('Defence Phase 5', 39), ('Defence Phase 8', 37), ('Mehmoodabad', 47), ('Manzoor Colony', 43), ('Liaquatabad', 34), ('Ancholi', 20), ('Nagan Chowrangi', 33), ('Sohrab Goth', 37), ('Shadman Town', 48), ('North Karachi', 21), ('Surjani Town', 43), ('Orangi Town', 27), ('Baldia Town', 36), ('Kemari', 33), ('Hawksbay', 27), ('Sea View', 21), ('Gizri', 29), ('Kharadar', 38), ('Garden East', 32), ('Garden West', 48), ('Jacob Lines', 37), ('Soldier Bazaar', 20), ('Lines Area', 5)],
    'Shadman Town': [('Clifton', 20), ('Saddar', 20), ('Lyari', 27), ('Korangi', 7), ('Landhi', 33), ('Malir', 23), ('Gulshan-e-Iqbal', 10), ('Gulistan-e-Johar', 6), ('North Nazimabad', 28), ('Nazimabad', 13), ('Federal B Area', 38), ('PECHS', 31), ('Shah Faisal Colony', 11), ('Model Colony', 11), ('Defence Phase 1', 17), ('Defence Phase 2', 19), ('Defence Phase 5', 31), ('Defence Phase 8', 26), ('Mehmoodabad', 36), ('Manzoor Colony', 43), ('Liaquatabad', 44), ('Ancholi', 12), ('Nagan Chowrangi', 29), ('Sohrab Goth', 40), ('New Karachi', 41), ('North Karachi', 28), ('Surjani Town', 16), ('Orangi Town', 7), ('Baldia Town', 15), ('Kemari', 28), ('Hawksbay', 26), ('Sea View', 20), ('Gizri', 22), ('Kharadar', 24), ('Garden East', 8), ('Garden West', 26), ('Jacob Lines', 16), ('Soldier Bazaar', 7), ('Lines Area', 36)],
    'North Karachi': [('Clifton', 6), ('Saddar', 7), ('Lyari', 50), ('Korangi', 7), ('Landhi', 19), ('Malir', 8), ('Gulshan-e-Iqbal', 24), ('Gulistan-e-Johar', 10), ('North Nazimabad', 50), ('Nazimabad', 46), ('Federal B Area', 6), ('PECHS', 46), ('Shah Faisal Colony', 42), ('Model Colony', 27), ('Defence Phase 1', 19), ('Defence Phase 2', 30), ('Defence Phase 5', 18), ('Defence Phase 8', 27), ('Mehmoodabad', 10), ('Manzoor Colony', 22), ('Liaquatabad', 28), ('Ancholi', 17), ('Nagan Chowrangi', 19), ('Sohrab Goth', 36), ('New Karachi', 46), ('Shadman Town', 19), ('Surjani Town', 23), ('Orangi Town', 44), ('Baldia Town', 18), ('Kemari', 5), ('Hawksbay', 46), ('Sea View', 26), ('Gizri', 43), ('Kharadar', 32), ('Garden East', 44), ('Garden West', 24), ('Jacob Lines', 38), ('Soldier Bazaar', 42), ('Lines Area', 13)],
    'Surjani Town': [('Clifton', 50), ('Saddar', 27), ('Lyari', 26), ('Korangi', 8), ('Landhi', 8), ('Malir', 22), ('Gulshan-e-Iqbal', 29), ('Gulistan-e-Johar', 18), ('North Nazimabad', 8), ('Nazimabad', 40), ('Federal B Area', 31), ('PECHS', 11), ('Shah Faisal Colony', 46), ('Model Colony', 7), ('Defence Phase 1', 21), ('Defence Phase 2', 27), ('Defence Phase 5', 41), ('Defence Phase 8', 14), ('Mehmoodabad', 33), ('Manzoor Colony', 11), ('Liaquatabad', 29), ('Ancholi', 13), ('Nagan Chowrangi', 42), ('Sohrab Goth', 30), ('New Karachi', 23), ('Shadman Town', 27), ('North Karachi', 15), ('Orangi Town', 36), ('Baldia Town', 32), ('Kemari', 10), ('Hawksbay', 16), ('Sea View', 48), ('Gizri', 49), ('Kharadar', 49), ('Garden East', 15), ('Garden West', 33), ('Jacob Lines', 19), ('Soldier Bazaar', 29), ('Lines Area', 39)],
    'Orangi Town': [('Clifton', 45), ('Saddar', 15), ('Lyari', 24), ('Korangi', 24), ('Landhi', 14), ('Malir', 16), ('Gulshan-e-Iqbal', 26), ('Gulistan-e-Johar', 47), ('North Nazimabad', 24), ('Nazimabad', 17), ('Federal B Area', 49), ('PECHS', 14), ('Shah Faisal Colony', 5), ('Model Colony', 27), ('Defence Phase 1', 44), ('Defence Phase 2', 39), ('Defence Phase 5', 43), ('Defence Phase 8', 22), ('Mehmoodabad', 25), ('Manzoor Colony', 50), ('Liaquatabad', 9), ('Ancholi', 25), ('Nagan Chowrangi', 33), ('Sohrab Goth', 5), ('New Karachi', 35), ('Shadman Town', 45), ('North Karachi', 18), ('Surjani Town', 14), ('Baldia Town', 41), ('Kemari', 9), ('Hawksbay', 14), ('Sea View', 30), ('Gizri', 46), ('Kharadar', 37), ('Garden East', 39), ('Garden West', 24), ('Jacob Lines', 9), ('Soldier Bazaar', 12), ('Lines Area', 27)],
    'Baldia Town': [('Clifton', 46), ('Saddar', 16), ('Lyari', 13), ('Korangi', 15), ('Landhi', 24), ('Malir', 39), ('Gulshan-e-Iqbal', 39), ('Gulistan-e-Johar', 26), ('North Nazimabad', 13), ('Nazimabad', 45), ('Federal B Area', 13), ('PECHS', 5), ('Shah Faisal Colony', 5), ('Model Colony', 29), ('Defence Phase 1', 44), ('Defence Phase 2', 17), ('Defence Phase 5', 5), ('Defence Phase 8', 13), ('Mehmoodabad', 36), ('Manzoor Colony', 42), ('Liaquatabad', 13), ('Ancholi', 36), ('Nagan Chowrangi', 42), ('Sohrab Goth', 18), ('New Karachi', 46), ('Shadman Town', 31), ('North Karachi', 15), ('Surjani Town', 24), ('Orangi Town', 17), ('Kemari', 11), ('Hawksbay', 44), ('Sea View', 19), ('Gizri', 32), ('Kharadar', 7), ('Garden East', 49), ('Garden West', 49), ('Jacob Lines', 38), ('Soldier Bazaar', 19), ('Lines Area', 29)],
    'Kemari': [('Clifton', 21), ('Saddar', 36), ('Lyari', 19), ('Korangi', 44), ('Landhi', 27), ('Malir', 35), ('Gulshan-e-Iqbal', 48), ('Gulistan-e-Johar', 50), ('North Nazimabad', 18), ('Nazimabad', 13), ('Federal B Area', 33), ('PECHS', 32), ('Shah Faisal Colony', 49), ('Model Colony', 5), ('Defence Phase 1', 11), ('Defence Phase 2', 37), ('Defence Phase 5', 5), ('Defence Phase 8', 43), ('Mehmoodabad', 13), ('Manzoor Colony', 20), ('Liaquatabad', 48), ('Ancholi', 19), ('Nagan Chowrangi', 30), ('Sohrab Goth', 11), ('New Karachi', 40), ('Shadman Town', 44), ('North Karachi', 35), ('Surjani Town', 32), ('Orangi Town', 17), ('Baldia Town', 40), ('Hawksbay', 10), ('Sea View', 49), ('Gizri', 31), ('Kharadar', 46), ('Garden East', 43), ('Garden West', 34), ('Jacob Lines', 14), ('Soldier Bazaar', 21), ('Lines Area', 15)],
    'Hawksbay': [('Clifton', 38), ('Saddar', 26), ('Lyari', 26), ('Korangi', 26), ('Landhi', 7), ('Malir', 36), ('Gulshan-e-Iqbal', 29), ('Gulistan-e-Johar', 23), ('North Nazimabad', 6), ('Nazimabad', 43), ('Federal B Area', 43), ('PECHS', 32), ('Shah Faisal Colony', 26), ('Model Colony', 22), ('Defence Phase 1', 11), ('Defence Phase 2', 43), ('Defence Phase 5', 40), ('Defence Phase 8', 30), ('Mehmoodabad', 21), ('Manzoor Colony', 40), ('Liaquatabad', 16), ('Ancholi', 17), ('Nagan Chowrangi', 5), ('Sohrab Goth', 23), ('New Karachi', 34), ('Shadman Town', 50), ('North Karachi', 48), ('Surjani Town', 16), ('Orangi Town', 13), ('Baldia Town', 20), ('Kemari', 47), ('Sea View', 37), ('Gizri', 11), ('Kharadar', 16), ('Garden East', 47), ('Garden West', 40), ('Jacob Lines', 36), ('Soldier Bazaar', 45), ('Lines Area', 19)],
    'Sea View': [('Clifton', 36), ('Saddar', 50), ('Lyari', 26), ('Korangi', 16), ('Landhi', 20), ('Malir', 8), ('Gulshan-e-Iqbal', 24), ('Gulistan-e-Johar', 49), ('North Nazimabad', 18), ('Nazimabad', 48), ('Federal B Area', 24), ('PECHS', 42), ('Shah Faisal Colony', 22), ('Model Colony', 47), ('Defence Phase 1', 24), ('Defence Phase 2', 7), ('Defence Phase 5', 36), ('Defence Phase 8', 15), ('Mehmoodabad', 33), ('Manzoor Colony', 31), ('Liaquatabad', 12), ('Ancholi', 9), ('Nagan Chowrangi', 10), ('Sohrab Goth', 29), ('New Karachi', 30), ('Shadman Town', 48), ('North Karachi', 26), ('Surjani Town', 30), ('Orangi Town', 48), ('Baldia Town', 50), ('Kemari', 35), ('Hawksbay', 25), ('Gizri', 49), ('Kharadar', 19), ('Garden East', 5), ('Garden West', 31), ('Jacob Lines', 26), ('Soldier Bazaar', 18), ('Lines Area', 19)],
    'Gizri': [('Clifton', 26), ('Saddar', 34), ('Lyari', 6), ('Korangi', 30), ('Landhi', 34), ('Malir', 49), ('Gulshan-e-Iqbal', 41), ('Gulistan-e-Johar', 20), ('North Nazimabad', 13), ('Nazimabad', 36), ('Federal B Area', 31), ('PECHS', 13), ('Shah Faisal Colony', 39), ('Model Colony', 18), ('Defence Phase 1', 10), ('Defence Phase 2', 20), ('Defence Phase 5', 23), ('Defence Phase 8', 37), ('Mehmoodabad', 31), ('Manzoor Colony', 24), ('Liaquatabad', 49), ('Ancholi', 12), ('Nagan Chowrangi', 21), ('Sohrab Goth', 29), ('New Karachi', 48), ('Shadman Town', 16), ('North Karachi', 33), ('Surjani Town', 32), ('Orangi Town', 44), ('Baldia Town', 46), ('Kemari', 48), ('Hawksbay', 12), ('Sea View', 6), ('Kharadar', 25), ('Garden East', 33), ('Garden West', 35), ('Jacob Lines', 14), ('Soldier Bazaar', 15), ('Lines Area', 39)],
    'Kharadar': [('Clifton', 48), ('Saddar', 8), ('Lyari', 35), ('Korangi', 33), ('Landhi', 14), ('Malir', 46), ('Gulshan-e-Iqbal', 32), ('Gulistan-e-Johar', 41), ('North Nazimabad', 43), ('Nazimabad', 19), ('Federal B Area', 26), ('PECHS', 50), ('Shah Faisal Colony', 6), ('Model Colony', 35), ('Defence Phase 1', 40), ('Defence Phase 2', 49), ('Defence Phase 5', 48), ('Defence Phase 8', 42), ('Mehmoodabad', 10), ('Manzoor Colony', 40), ('Liaquatabad', 14), ('Ancholi', 11), ('Nagan Chowrangi', 42), ('Sohrab Goth', 49), ('New Karachi', 40), ('Shadman Town', 11), ('North Karachi', 17), ('Surjani Town', 49), ('Orangi Town', 27), ('Baldia Town', 43), ('Kemari', 44), ('Hawksbay', 26), ('Sea View', 6), ('Gizri', 34), ('Garden East', 38), ('Garden West', 41), ('Jacob Lines', 5), ('Soldier Bazaar', 11), ('Lines Area', 38)],
    'Garden East': [('Clifton', 50), ('Saddar', 39), ('Lyari', 39), ('Korangi', 48), ('Landhi', 33), ('Malir', 12), ('Gulshan-e-Iqbal', 27), ('Gulistan-e-Johar', 40), ('North Nazimabad', 8), ('Nazimabad', 16), ('Federal B Area', 12), ('PECHS', 33), ('Shah Faisal Colony', 19), ('Model Colony', 32), ('Defence Phase 1', 47), ('Defence Phase 2', 22), ('Defence Phase 5', 46), ('Defence Phase 8', 26), ('Mehmoodabad', 34), ('Manzoor Colony', 18), ('Liaquatabad', 24), ('Ancholi', 45), ('Nagan Chowrangi', 49), ('Sohrab Goth', 31), ('New Karachi', 31), ('Shadman Town', 14), ('North Karachi', 35), ('Surjani Town', 15), ('Orangi Town', 35), ('Baldia Town', 10), ('Kemari', 10), ('Hawksbay', 18), ('Sea View', 23), ('Gizri', 14), ('Kharadar', 29), ('Garden West', 13), ('Jacob Lines', 40), ('Soldier Bazaar', 40), ('Lines Area', 17)],
    'Garden West': [('Clifton', 6), ('Saddar', 8), ('Lyari', 49), ('Korangi', 47), ('Landhi', 28), ('Malir', 44), ('Gulshan-e-Iqbal', 48), ('Gulistan-e-Johar', 37), ('North Nazimabad', 5), ('Nazimabad', 46), ('Federal B Area', 19), ('PECHS', 35), ('Shah Faisal Colony', 26), ('Model Colony', 43), ('Defence Phase 1', 37), ('Defence Phase 2', 47), ('Defence Phase 5', 48), ('Defence Phase 8', 43), ('Mehmoodabad', 11), ('Manzoor Colony', 20), ('Liaquatabad', 22), ('Ancholi', 37), ('Nagan Chowrangi', 8), ('Sohrab Goth', 37), ('New Karachi', 50), ('Shadman Town', 13), ('North Karachi', 29), ('Surjani Town', 41), ('Orangi Town', 44), ('Baldia Town', 39), ('Kemari', 22), ('Hawksbay', 26), ('Sea View', 6), ('Gizri', 50), ('Kharadar', 8), ('Garden East', 27), ('Jacob Lines', 45), ('Soldier Bazaar', 23), ('Lines Area', 9)],
    'Jacob Lines': [('Clifton', 20), ('Saddar', 23), ('Lyari', 41), ('Korangi', 48), ('Landhi', 48), ('Malir', 27), ('Gulshan-e-Iqbal', 34), ('Gulistan-e-Johar', 32), ('North Nazimabad', 33), ('Nazimabad', 19), ('Federal B Area', 36), ('PECHS', 29), ('Shah Faisal Colony', 6), ('Model Colony', 14), ('Defence Phase 1', 26), ('Defence Phase 2', 37), ('Defence Phase 5', 5), ('Defence Phase 8', 42), ('Mehmoodabad', 43), ('Manzoor Colony', 46), ('Liaquatabad', 28), ('Ancholi', 37), ('Nagan Chowrangi', 26), ('Sohrab Goth', 27), ('New Karachi', 40), ('Shadman Town', 40), ('North Karachi', 11), ('Surjani Town', 35), ('Orangi Town', 9), ('Baldia Town', 12), ('Kemari', 6), ('Hawksbay', 33), ('Sea View', 49), ('Gizri', 47), ('Kharadar', 48), ('Garden East', 21), ('Garden West', 47), ('Soldier Bazaar', 36), ('Lines Area', 46)],
    'Soldier Bazaar': [('Clifton', 19), ('Saddar', 18), ('Lyari', 48), ('Korangi', 12), ('Landhi', 38), ('Malir', 6), ('Gulshan-e-Iqbal', 47), ('Gulistan-e-Johar', 28), ('North Nazimabad', 27), ('Nazimabad', 46), ('Federal B Area', 24), ('PECHS', 36), ('Shah Faisal Colony', 49), ('Model Colony', 31), ('Defence Phase 1', 22), ('Defence Phase 2', 6), ('Defence Phase 5', 25), ('Defence Phase 8', 27), ('Mehmoodabad', 24), ('Manzoor Colony', 10), ('Liaquatabad', 49), ('Ancholi', 43), ('Nagan Chowrangi', 8), ('Sohrab Goth', 37), ('New Karachi', 40), ('Shadman Town', 13), ('North Karachi', 9), ('Surjani Town', 6), ('Orangi Town', 40), ('Baldia Town', 50), ('Kemari', 29), ('Hawksbay', 48), ('Sea View', 46), ('Gizri', 29), ('Kharadar', 28), ('Garden East', 33), ('Garden West', 39), ('Jacob Lines', 42), ('Lines Area', 15)],
    'Lines Area': [('Clifton', 31), ('Saddar', 34), ('Lyari', 31), ('Korangi', 10), ('Landhi', 23), ('Malir', 31), ('Gulshan-e-Iqbal', 45), ('Gulistan-e-Johar', 43), ('North Nazimabad', 30), ('Nazimabad', 34), ('Federal B Area', 32), ('PECHS', 18), ('Shah Faisal Colony', 49), ('Model Colony', 24), ('Defence Phase 1', 30), ('Defence Phase 2', 30), ('Defence Phase 5', 9), ('Defence Phase 8', 34), ('Mehmoodabad', 37), ('Manzoor Colony', 29), ('Liaquatabad', 44), ('Ancholi', 44), ('Nagan Chowrangi', 18), ('Sohrab Goth', 30), ('New Karachi', 41), ('Shadman Town', 36), ('North Karachi', 14), ('Surjani Town', 41), ('Orangi Town', 40), ('Baldia Town', 5), ('Kemari', 31), ('Hawksbay', 48), ('Sea View', 19), ('Gizri', 42), ('Kharadar', 11), ('Garden East', 50), ('Garden West', 48), ('Jacob Lines', 16), ('Soldier Bazaar', 15)]
}   

def heuristic(node, goal, area_coords, graph):
    if node not in area_coords or goal not in area_coords:
        return float('inf')

    node_coords = area_coords[node]
    goal_coords = area_coords[goal]

    dx = abs(node_coords[0] - goal_coords[0])
    dy = abs(node_coords[1] - goal_coords[1])
    euclidean_distance = math.sqrt(dx ** 2 + dy ** 2)

    direct_road_distance = float('inf')
    for neighbor, distance in graph.get(node, []):
        if neighbor == goal:
            direct_road_distance = distance
            break

    traffic_factor = random.uniform(1.0, 3.0) 

    heuristic_value = 0.6 * euclidean_distance + 0.4 * direct_road_distance * traffic_factor

    return heuristic_value

def a_star(start, goal, area_coords, graph):
    open_set = PriorityQueue()
    open_set.put((0, start))  # (f_score, node)
    
    came_from = {}  # To track the optimal path
    g_score = {market: float('inf') for market in area_coords}  # Cost to reach each node
    f_score = {market: float('inf') for market in area_coords}  # Estimated total cost (g + heuristic)

    g_score[start] = 0  # Starting point has 0 cost
    f_score[start] = heuristic(start, goal, area_coords, graph)  # Starting point heuristic

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            # Reconstruct the path from goal to start
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return reversed path

        # Explore neighbors of the current node
        for neighbor, cost in graph[current]:
            tentative_g_score = g_score[current] + cost  # Tentative cost to reach the neighbor

            if tentative_g_score < g_score[neighbor]:  # If a better path to the neighbor is found
                came_from[neighbor] = current  # Record the path
                g_score[neighbor] = tentative_g_score  # Update the g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal, area_coords, graph)  # Update the f_score

                # Only add to the open set if not already there (or if it's a better path)
                if neighbor not in [i[1] for i in open_set.queue]:
                    open_set.put((f_score[neighbor], neighbor))

    return None



def plot_map(path, assignment=None):
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_facecolor('#ecf0f1')
    
    # Plot all areas with colors if assignment exists
    for market, coords in area_coords.items():
        color = assignment.get(market, 'gray') if assignment else '#2c3e50'
        ax.scatter(coords[1], coords[0], color=color, s=100, edgecolors='white', zorder=3)
        ax.text(coords[1], coords[0], market, fontsize=8, ha='center', va='center')
    
    # Plot path if it exists
    if path:
        for i in range(len(path) - 1):
            start_market = path[i]
            end_market = path[i + 1]
            start_coords = area_coords[start_market]
            end_coords = area_coords[end_market]
            ax.plot([start_coords[1], end_coords[1]], [start_coords[0], end_coords[0]], 
                    color='green', linewidth=2, zorder=2)

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Karachi Map')
    st.pyplot(fig)

colors = ['Red', 'Green', 'Blue']

def is_valid(assignment, area, color):
    for neighbor in graph[area]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    
    # Get current area coordinates
    current_lat, current_lon = area_coords[area]
    
    # Check areas in same column (same longitude)
    for other_area, coords in area_coords.items():
        if other_area != area and other_area in assignment:
            other_lat, other_lon = coords
            # Same column (longitude)
            if abs(other_lon - current_lon) < 0.0001:
                if assignment[other_area] == color:
                    return False
            # Same row (latitude)
            if abs(other_lat - current_lat) < 0.0001:
                if assignment[other_area] == color:
                    return False
            # Diagonal (both lat and lon are close)
            if (abs(other_lon - current_lon) < 0.0001 and 
                abs(other_lat - current_lat) < 0.0001):
                if assignment[other_area] == color:
                    return False
    
    return True

def get_remaining_colors(assignment, area):
    used_colors = set()
    current_lat, current_lon = area_coords[area]
    
    # Check graph neighbors
    for neighbor in graph[area]:
        if neighbor in assignment:
            used_colors.add(assignment[neighbor])
    
    # Check same column, row, and diagonal
    for other_area, coords in area_coords.items():
        if other_area != area and other_area in assignment:
            other_lat, other_lon = coords
            # Same column
            if abs(other_lon - current_lon) < 0.0001:
                used_colors.add(assignment[other_area])
            # Same row
            if abs(other_lat - current_lat) < 0.0001:
                used_colors.add(assignment[other_area])
            # Diagonal
            if (abs(other_lon - current_lon) < 0.0001 and 
                abs(other_lat - current_lat) < 0.0001):
                used_colors.add(assignment[other_area])
    
    return [c for c in colors if c not in used_colors]

def backtrack(assignment):
    if len(assignment) == len(area_coords):
        return assignment  # All areas are assigned

    # Select the unassigned variable with the fewest remaining values (MRV heuristic)
    unassigned = [area for area in area_coords if area not in assignment]
    area = min(unassigned, key=lambda a: len(get_remaining_colors(assignment, a)))

    # Try colors in order of least constraining value
    for color in sorted(get_remaining_colors(assignment, area), 
                       key=lambda c: count_conflicts(assignment, area, c)):
        if is_valid(assignment, area, color):
            assignment[area] = color
            result = backtrack(assignment)
            if result:
                return result
            del assignment[area]

    return None

def count_conflicts(assignment, area, color):
    """Count how many other areas would conflict if this color were chosen"""
    conflicts = 0
    current_lat, current_lon = area_coords[area]
    
    # Check graph neighbors
    for neighbor in graph[area]:
        if neighbor in assignment and assignment[neighbor] == color:
            conflicts += 1
    
    # Check same column, row, and diagonal
    for other_area, coords in area_coords.items():
        if other_area != area and other_area in assignment:
            other_lat, other_lon = coords
            if assignment[other_area] == color:
                # Same column
                if abs(other_lon - current_lon) < 0.0001:
                    conflicts += 1
                # Same row
                if abs(other_lat - current_lat) < 0.0001:
                    conflicts += 1
                # Diagonal
                if (abs(other_lon - current_lon) < 0.0001 and 
                    abs(other_lat - current_lat) < 0.0001):
                    conflicts += 1
    
    return conflicts

# Streamlit UI setup
st.title("Pathfinding App with CSP Coloring")

# User input for start and goal markets
start_market = st.selectbox("Select the start market", list(area_coords.keys()))
goal_market = st.selectbox("Select the destination market", list(area_coords.keys()))

# Button to calculate the path
if st.button("Find Path"):
    if start_market == goal_market:
        st.write("Start and goal markets are the same. Please select different markets.")
    else:
        
        path = a_star(start_market, goal_market, area_coords, graph)
        if path:
            st.markdown(f"""
                    <div class="result-container">
                        <p>🚩 <strong>Path from</strong> <span class="path-highlight">{start_market}</span> 
                        <strong>to</strong> <span class="path-highlight">{goal_market}</span>:</p>
                        <p style="margin-top:0.5rem;">🧭 {" → ".join(path)}</p>
                    </div>
                """, unsafe_allow_html=True)
            solution = backtrack({})
            plot_map(path,solution)  # Display map with the path

        else:
            st.write(f"No path found between {start_market} and {goal_market}.")
```
