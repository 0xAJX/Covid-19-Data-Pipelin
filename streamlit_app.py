import re
from os import listdir
from os.path import isfile, join
import numpy as np
import streamlit as st
import pandas as pd
import datetime

st.write("Here's our first attempt at using data to create a table:")

files = [f for f in listdir("ClimateChangeModified") if isfile(join("ClimateChangeModified", f))]

dataFrame = None

for f in files:
    if re.search(".csv$", f):
        dataFrame = pd.read_csv("ClimateChangeModified/" + f, names=["date", "death"])

if dataFrame is None:
    raise Exception("Issue with reading file")

df = dataFrame
df.set_index('date', inplace=True)
st.area_chart(df.loc['03-03-2020':])