import pandas as pd
import streamlit as st


def space(num_lines=1):
    """Return the required number of spaced lines."""
    for _ in range(num_lines):
        st.write("")
