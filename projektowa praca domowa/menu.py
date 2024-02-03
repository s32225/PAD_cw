import streamlit as st 
import numpy as np
import pandas as pd
from streamlit_option_menu import option_menu
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.graph_objects as go   


data = pd.read_csv('messy_data.csv')
data.columns = data.columns.str.replace(' ', '')
data_cleaned = pd.read_csv('data_cleaned.csv', sep=',')
data_no_outliers = pd.read_csv('data_no_outliers.csv', sep=',')
diamond_clean_data_standard = pd.read_csv('diamond_clean_data_standarized.csv', sep=',')

X = diamond_clean_data_standard.drop(["price"],axis=1)
y = diamond_clean_data_standard.price
R2_Scores = []

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

while len(X.columns) > 1:
    p_values = model.pvalues[1:]
    max_p_value = p_values.max()
    if max_p_value > 0.05: 
        remove_feature = p_values.idxmax()
        X = X.drop(remove_feature, axis=1)
        model = sm.OLS(y, X).fit()
    else:
        break

print(model.summary())  

residuals = model.resid
y_pred = model.predict(X)

feature_importances = pd.DataFrame({'Feature': X.columns[1:], 'Coefficient': model.params[1:]})
feature_importances['Importance'] = np.abs(feature_importances['Coefficient']) / np.abs(feature_importances['Coefficient']).sum()
feature_importances_sorted = feature_importances.sort_values(by='Importance', ascending=False)

with st.sidebar:
    selected = option_menu(
        menu_title='Menu główne',
        options = ['Dane', 'Boxplot','Histograms', 'Violin plot', 'Pie Charts', 'Correlation Matrix', 'Model'], 
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


    scatter_fig = px.scatter(data, x=selected_x, y=selected_y, title=f"Scatter Plot: {selected_x} vs {selected_y}")
    st.plotly_chart(scatter_fig)

elif selected == 'Dane' and data_option == 'Oczyszczone':

    st.title("Wizualizacja w celu wstępnej oceny danych")
    selected_x_clean = st.selectbox("Wybierz zmienną na osi X:", data_cleaned.columns)
    selected_y_clean = st.selectbox("Wybierz zmienną na osi Y:", data_cleaned.columns[::-1])
    st.subheader(f" Scatterplot dla zmiennych {selected_x_clean} i {selected_y_clean}")


    scatter_fig = px.scatter(data_cleaned, x=selected_x_clean, y=selected_y_clean, title=f"Scatter Plot: {selected_x_clean} vs {selected_y_clean}")
    st.plotly_chart(scatter_fig)


if selected == 'Boxplot':
    data_option = st.selectbox('Wybierz rodzaj danych:', ['Przed usuwaniem Outliersów', 'Po usuwaniu Outliersów'])
    if data_option == 'Przed usuwaniem Outliersów':
        st.subheader("Interaktywny Box Plot dla jednej zmiennej przed usuwaniem outliersów")

        selected_variable = st.selectbox("Wybierz zmienną:", data_cleaned.columns[1:])

        box_fig = px.box(data_cleaned, y=selected_variable, title=f"Box Plot dla zmiennej: {selected_variable}")
        st.plotly_chart(box_fig)

    elif data_option == 'Po usuwaniu Outliersów':  
        st.subheader("Interaktywny Box Plot dla jednej zmiennej po usuwaniu outliersów")

        selected_variable = st.selectbox("Wybierz zmienną:", data_no_outliers.columns[1:])

        box_fig = px.box(data_no_outliers, y=selected_variable, title=f"Box Plot dla zmiennej: {selected_variable}")
        st.plotly_chart(box_fig)

if selected == 'Histograms':
    st.title('Histogramy dla wybranych zmiennych')
    selected_clean = st.selectbox("Wybierz zmienną:", data_no_outliers.columns)
    hst = px.histogram(data_no_outliers, x=selected_clean, title=f"Histogram dla zmiennej: {selected_clean}")
    st.plotly_chart(hst)

if selected == 'Violin plot':
    st.title('Violin ploty dla wybranych zmiennych kategorycznych')
    selected_variable = st.selectbox("Wybierz zmienną kategoryczną:", ['cut', 'color', 'clarity'])

    st.write(f"Selected Variable: {selected_variable}")

    violin_fig = px.violin(data_no_outliers, x=selected_variable, y='price', box=True, points="all", title=f"Violin Plot - Price vs {selected_variable}", color=selected_variable)
    violin_fig.update_layout(xaxis=dict(title=selected_variable), yaxis=dict(title="Price"))

    st.plotly_chart(violin_fig)

if selected == 'Pie Charts':
    st.title('Pie Charts dla wybranych zmiennych kategorycznych')
    selected_variable = st.selectbox("Wybierz zmienną kategoryczną:", ['cut', 'color', 'clarity'])

    st.write(f"Selected Variable: {selected_variable}")

    pie_fig = px.pie(data_no_outliers, names=selected_variable, title=f"Pie Chart - Price vs {selected_variable}", color=selected_variable)
    pie_fig.update_layout(xaxis=dict(title=selected_variable), yaxis=dict(title="Price"))

    st.plotly_chart(pie_fig)

correlation_matrix = diamond_clean_data_standard.corr()
if selected == 'Correlation Matrix':
    fig = ff.create_annotated_heatmap(
        z=correlation_matrix.values,
        x=list(correlation_matrix.columns),
        y=list(correlation_matrix.index),
        colorscale='Viridis',
        annotation_text=correlation_matrix.round(2).values,
        showscale=True,
    )

    fig.update_layout(
        title="Correlation Matrix",
        xaxis=dict(title="Features"),
        yaxis=dict(title="Features"),
        autosize=False,
        width=1000,
        height=1000,
        font=dict(size=8), 
    )

    st.plotly_chart(fig)

if selected == 'Model':

    fig_feature_importances = go.Figure()

    fig_feature_importances.add_trace(go.Bar(
        y=feature_importances_sorted['Feature'],  
        x=feature_importances_sorted['Importance'],  
        orientation='h',  
        marker=dict(color='skyblue'),  
    ))


    fig_feature_importances.update_layout(
        title='Feature Importances', 
        xaxis=dict(title='Importance'),  
        yaxis=dict(title='Feature'), 
    )


    viz_data = pd.DataFrame({'Fitted Values': model.fittedvalues, 'Residuals': model.resid})

    fig_residuals = px.scatter(viz_data, x='Fitted Values', y='Residuals', labels={'Residuals': 'Residuals'})

    fig_residuals.add_trace(go.Scatter(x=[min(viz_data['Fitted Values']), max(viz_data['Fitted Values'])],
                                    y=[0, 0],
                                    mode='lines',
                                    name='Zero Line',
                                    line=dict(color='red', dash='dash')))



    with st.expander("Feature Importances"):
        st.plotly_chart(fig_feature_importances)

    with st.expander("Residuals"):
        st.plotly_chart(fig_residuals)