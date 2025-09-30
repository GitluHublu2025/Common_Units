import streamlit as st
from conversions_common import conversion_map
import pandas as pd

st.set_page_config(page_title="Common Units Converter (Python dict)", layout="centered")
st.title("Units Converter — Perry Handbook")

# Select input unit
from_unit = st.radio("Select input unit (From):", list(conversion_map.keys()))

# Show only valid "To" options
to_options = list(conversion_map[from_unit].keys())
if len(to_options) <= 8:
    to_unit = st.radio("Convert to:", to_options)
else:
    to_unit = st.selectbox("Convert to:", to_options)

# Input value
value = st.number_input("Value (numeric):", value=1.0, format="%.12g")

# Convert
if st.button("Convert"):
    factor = conversion_map[from_unit][to_unit]
    result = value * factor
    st.success(f"{value} {from_unit} = {result} {to_unit}")
    st.write(f"Factor used: {factor} (multiply input by this factor)")

st.markdown("---")
st.write("Notes:")
st.write("• Units are kept exactly as they appear in *Common Units.pdf*")
st.write("• Only conversions with explicit multiply-by factors are included")

# Allow CSV download of the conversion table
rows = []
for fu, d in conversion_map.items():
    for tu, f in d.items():
        rows.append({"from": fu, "to": tu, "factor": f})
df = pd.DataFrame(rows)

@st.cache_data
def get_csv_bytes():
    return df.to_csv(index=False).encode('utf-8')

st.download_button("Download conversion table (CSV)",
                   data=get_csv_bytes(),
                   file_name="conversions_common.csv",
                   mime="text/csv")

