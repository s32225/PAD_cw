import streamlit as st 
import pandas as pd
from streamlit_option_menu import option_menu
import seaborn as sns
import plotly.express as px

data = pd.read_csv('C:\Python\PAD_cw\projektowa praca domowa\messy_data.csv')
data.columns = data.columns.str.replace(' ', '')
data_cleaned = pd.read_csv('C:\Python\PAD_cw\projektowa praca domowa\data_cleaned.csv', sep=',')
data_no_outliers = pd.read_csv('C:\Python\PAD_cw\projektowa praca domowa\data_no_outliers.csv', sep=',')

with st.sidebar:
    selected = option_menu(
        menu_title='Menu główne',
        options = ['Dane', 'Boxplot','Histogramy', 'Violin plot'], 
        icons= ['house', 'book', 'envelope'],
        menu_icon = 'cast',
        default_index=0 
    )

if selected == 'Dane':
    st.title(f'Podgląd danych')
    data_option = st.selectbox('Wybierz rodzaj danych:', ['Nieoczyszczone', 'Oczyszczone'])
    if data_option == 'Nieoczyszczone':
        st.write("Dane nieoczyszczone:")
        st.write(data)
        st.write("Podstawowe informacje o danych")
        st.write(data.describe(include='all'))
    elif data_option == 'Oczyszczone':
        st.write("Dane oczyszczone:")
        st.write(data_cleaned)
        st.write("Podstawowe informacje o danych")
        st.write(data_cleaned.describe(include='all'))


if selected == 'Dane' and data_option == 'Nieoczyszczone':

    st.title("Wizualizacja w celu wstępnej oceny danych")
    selected_x = st.selectbox("Wybierz zmienną na osi X:", data.columns)
    selected_y = st.selectbox("Wybierz zmienną na osi Y:", data.columns[::-1])
    st.subheader(f" Scatterplot dla zmiennych {selected_x} i {selected_y}")


    # Interaktywny Scatter Plot
    scatter_fig = px.scatter(data, x=selected_x, y=selected_y, title=f"Scatter Plot: {selected_x} vs {selected_y}")
    st.plotly_chart(scatter_fig)

elif selected == 'Dane' and data_option == 'Oczyszczone':

    st.title("Wizualizacja w celu wstępnej oceny danych")
    selected_x_clean = st.selectbox("Wybierz zmienną na osi X:", data_cleaned.columns)
    selected_y_clean = st.selectbox("Wybierz zmienną na osi Y:", data_cleaned.columns[::-1])
    st.subheader(f" Scatterplot dla zmiennych {selected_x_clean} i {selected_y_clean}")


    # Interaktywny Scatter Plot
    scatter_fig = px.scatter(data_cleaned, x=selected_x_clean, y=selected_y_clean, title=f"Scatter Plot: {selected_x_clean} vs {selected_y_clean}")
    st.plotly_chart(scatter_fig)


if selected == 'Boxplot':
    data_option = st.selectbox('Wybierz rodzaj danych:', ['Przed usuwaniem Outliersów', 'Po usuwaniu Outliersów'])
    if data_option == 'Przed usuwaniem Outliersów':
        st.subheader("Interaktywny Box Plot dla jednej zmiennej przed usuwaniem outliersów")

        selected_variable = st.selectbox("Wybierz zmienną:", data_cleaned.columns[1:])

        # Interaktywny Box Plot
        box_fig = px.box(data_cleaned, y=selected_variable, title=f"Box Plot dla zmiennej: {selected_variable}")
        st.plotly_chart(box_fig)

    elif data_option == 'Po usuwaniu Outliersów':  
        st.subheader("Interaktywny Box Plot dla jednej zmiennej po usuwaniu outliersów")

        selected_variable = st.selectbox("Wybierz zmienną:", data_no_outliers.columns[1:])

        # Interaktywny Box Plot
        box_fig = px.box(data_no_outliers, y=selected_variable, title=f"Box Plot dla zmiennej: {selected_variable}")
        st.plotly_chart(box_fig)

if selected == 'Histogramy':
    st.title('Histogramy dla wybranych zmiennych')
    selected_clean = st.selectbox("Wybierz zmienną:", data_no_outliers.columns)
    hst = px.histogram(data_no_outliers, x=selected_clean, title=f"Histogram dla zmiennej: {selected_clean}")
    st.plotly_chart(hst)

if selected == 'Violin plot':
    st.title('Violin ploty dla wybranych zmiennych kategorycznych')
    selected_variable = st.selectbox("Wybierz zmienną kategoryczną:", ['cut', 'color', 'clarity'])

    # Debugging: Check the selected variable
    st.write(f"Selected Variable: {selected_variable}")

    # Interaktywny Violin Plot
    violin_fig = px.violin(data_no_outliers, x=selected_variable, y='price', box=True, points="all", title=f"Violin Plot - Price vs {selected_variable}", color=selected_variable)
    violin_fig.update_layout(xaxis=dict(title=selected_variable), yaxis=dict(title="Price"))

    # Debugging: Display the violin plot
    st.plotly_chart(violin_fig)
