import streamlit as st
import altair as alt
from vega_datasets import data


def import_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source
