import streamlit as st
import altair as alt
from data.data_import import import_data
from features.data_viz import get_chart
# import mysql.connector
# import redshift_connector
from user import login
import pandas as pd

st.set_page_config(
    layout="wide", page_icon='assets/heineken_1.jpeg',
    page_title='Heineken Brewery')

# st.header("Heineken Brewhouse Report 🍻 ")


headerSection = st.container()
mainSection = st.container()
LoginSection = st.container()
LogoutSection = st.container()


def show_main_page():

    with mainSection:
        df_enchimento = pd.DataFrame({'Headspace': 'null', 'Extrato Inicial': 'null',
                                     'Volume Inicial': 'null', 'ph 48 horas': 'null', 'Volume SAP': 'null'}, index=['Headspace', 'Extrato Inicial',
                                     'Volume Inicial', 'ph 48 horas', 'Volume SAP'])
        # df_qtd_malte = pd.read_csv("data/df_qtd_malte.csv", sep=',')
        # df_coz_malte = pd.read_csv("data/df_coz_malte.csv", sep=',')

        source = import_data()

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
        data_container = st.container()
        with data_container:
            c1, c2 = st.columns(
                [2, 1], gap="small")
            with c1:
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    st.text_input("Tanque(OD)", value=27)
                with b2:
                    st.text_input("Tanque(OD)")
                with b3:
                    st.text_input("Zero Grau")
                with b4:
                    st.text_input("Guarda Quente")

                # Display both charts together
                st.altair_chart((chart + annotation_layer).interactive(),
                                use_container_width=True)
                st.dataframe(df_enchimento.reset_index(drop=True))

            with c2:
                add_data = st.button("Salvar ✅", use_container_width=True)
                st.subheader("Dados de Enchimento")
                headspace = st.text_input("Headspace")
                ext_ini = st.text_input("Extrato Inicial")

        st.sidebar.image('assets/Heineken-Logo-PNG4.png',
                         use_column_width=True)
        st.sidebar.header("Inputs")

        Inicio_Ben = st.sidebar.text_input("Data Início")
        Fim_Ben = st.sidebar.text_input("Data Fim")
        Ench_tanque = st.sidebar.text_input("Enchimento Tanque")
        # Qtd_Silo2 = options_form.text_input("Qtd_Silo2")
        st.sidebar.write("Status")
        st.sidebar.checkbox('Todos')
        st.sidebar.checkbox('Disponíveis')
        st.sidebar.checkbox('Finalizados')
        st.sidebar.checkbox('Reprovados')

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
