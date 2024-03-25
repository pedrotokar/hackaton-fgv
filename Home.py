import streamlit as st
import pandas as pd
import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json

from default import default_style

default_style()

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)




