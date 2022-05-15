import re
from os import listdir
from os.path import isfile, join
import numpy as np
import streamlit as st
import pandas as pd
import datetime

st.write("Monthly Deaths Caused By Covid-19")
working_directory = "CovidModified"
files = [f for f in listdir(working_directory) if isfile(join(working_directory, f))]

df = None

for f in files:
    if re.search(".csv$", f):
        df = pd.read_csv(working_directory + "/" + f, names=["date", "death"])

if df is None:
    raise Exception("Issue with reading file")

df.set_index('date', inplace=True)
st.area_chart(df)