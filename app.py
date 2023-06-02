import streamlit as st
import altair as alt
from datetime import datetime
# import mysql.connector
# import redshift_connector
from user import login
import pandas as pd
from vega_datasets import data

st.set_page_config(
    layout="centered", page_icon='assets/heineken_1.jpeg',
    page_title='Heineken Brewery')

st.header("Heineken Brewhouse Report 🍻 ")

st.write('This is a web app to generate automated reports from Heineken\
            Brewery.')


headerSection = st.container()
mainSection = st.container()
LoginSection = st.container()
LogoutSection = st.container()


def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source


def get_chart(data):

    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolution of stock prices")
        .mark_line()
        .encode(
            x="date",
            y="price",
            color="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


def show_main_page():

    with mainSection:

        df_qtd_malte = pd.read_csv("data/df_qtd_malte.csv", sep=',')
        df_coz_malte = pd.read_csv("data/df_coz_malte.csv", sep=',')

        source = get_data()

        # Original time series chart. Omitted `get_chart` for clarity
        chart = get_chart(source)

        # Input annotations
        ANNOTATIONS = [
            ("Mar 01, 2008", "Pretty good day for GOOG"),
            ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
            ("Nov 01, 2008", "Market starts again thanks to..."),
            ("Dec 01, 2009", "Small crash for GOOG after..."),
        ]

        # Create a chart with annotations
        annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
        annotations_df.date = pd.to_datetime(annotations_df.date)
        annotations_df["y"] = 0
        annotation_layer = (
            alt.Chart(annotations_df)
            .mark_text(size=15, text="⬇", dx=0, dy=-10, align="center")
            .encode(
                x="date:T",
                y=alt.Y("y:Q"),
                tooltip=["event"],
            )
            .interactive()
        )

        # Display both charts together
        st.altair_chart((chart + annotation_layer).interactive(),
                        use_container_width=True)

        st.subheader("Batch Number: 1234")

        st.subheader("Malt Amount")
        st.table(df_qtd_malte.tail())

        st.subheader("Malt Mash Tun")
        st.table(df_coz_malte.tail())

        st.sidebar.image('assets/heineken_logo.png',
                         use_column_width=True)
        st.sidebar.header("Inputs")
        options_form = st.sidebar.form("options_form")

        Inicio_Ben = options_form.text_input("Inicio_Ben")
        Fim_Ben = options_form.text_input("Fim_Ben")
        Qtd_Silo1 = options_form.text_input("Qtd_Silo1")
        Qtd_Silo2 = options_form.text_input("Qtd_Silo2")

        Inicio_CozMal = options_form.text_input("Inicio_CozMal")
        Fim_CozMal = options_form.text_input("Fim_CozMal")
        Temp_Max_CozMal = options_form.text_input("Temp_Max_CozMal")
        Dur_CozMal = options_form.text_input("Dur_CozMal")

        add_data = options_form.form_submit_button()

        if add_data:
            new_data_malte = {
                "Inicio_Ben": Inicio_Ben,
                "Fim_Ben": Fim_Ben,
                "Qtd_Silo1": Qtd_Silo1,
                "Qtd_Silo2": Qtd_Silo2}

            new_data_coz_malte = {
                "Inicio_CozMal": Inicio_CozMal,
                "Fim_CozMal": Fim_CozMal,
                "Temp_Max_CozMal": Temp_Max_CozMal,
                "Dur_CozMal": Dur_CozMal}
            df_qtd_malte = pd.concat([df_qtd_malte, pd.DataFrame(
                [new_data_malte])], ignore_index=True)
            df_coz_malte = pd.concat([df_coz_malte, pd.DataFrame(
                [new_data_coz_malte])], ignore_index=True)
            df_qtd_malte.to_csv("data/df_qtd_malte.csv", index=False)
            df_coz_malte.to_csv("data/df_coz_malte.csv", index=False)


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False


def show_logout_page():
    LoginSection.empty()
    with LogoutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def show_login_page():
    with LoginSection:
        st.image('assets/heineken_logo.png', use_column_width=True)
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(
                label="", value="", placeholder="Enter your user name")
            password = st.text_input(
                label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked,
                      args=(userName, password))


with headerSection:
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn']:
            show_logout_page()
            show_main_page()
        else:
            show_login_page()
