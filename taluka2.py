import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np


st.set_page_config(page_title=" 📊PMBFY Claim Analysis",layout="wide")
st.markdown(
    """
   <style>
        .stApp { background-color: #E3F2FD; }  /* Light Sky Blue */
        section[data-testid="stSidebar"] { background-color: #BBDEFB; }  /* Soft Blue */
        .block-container { background-color: #ffffff; padding: 20px; border-radius: 15px; }
        .header-title { text-align: center; font-size: 3.5rem; color: #0D47A1; font-weight: bold; text-shadow: 3px 3px 5px #1976D2; }
        .header-subtitle { text-align: center; font-size: 2rem; color: #1E88E5; font-style: italic; text-shadow: 2px 2px 4px #64B5F6; }
        .header-intern { text-align: center; font-size: 1.5rem; color: #0D47A1; font-weight: bold; }
    </style>

    """,
    unsafe_allow_html=True
)

df=pd.read_excel("PMFBY Taluka wise 2018-2023.xlsx")
def header_page():
    st.markdown("<h1 style='text-align: center,color: black;'>📊 PMFBY Analysis 2018-2023</h1>",unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center,color: black;'>By Sharvari Aware</h2>",unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center,color: black;'>Data Science Intern</h3>",unsafe_allow_html=True)
f1=st.file_uploader(":file_folder:Upload a file",type=['xlsx','xls'])
if f1 is not None:
    filename=f1.name
    st.write(filename)

    df=pd.read_excel(f1,engine="openpyxl")
else:
    st.markdown("Please upload a file")


def Year_Wise_Analysis():
    st.title("Year Wise Analysis PMFBY 2018-2023")
    st.sidebar.header("Year Wise Analysis")

    district = st.sidebar.multiselect("Select District:", options=df['District Name'].unique(),default=df['District Name'].unique())
    #taluka = st.sidebar.multiselect("Select Taluka:", options=df['Taluka Name'].unique(),default=df['Taluka Name'].unique())
#1
    df_selection1 = df[(df['District Name'].isin(district))]
    taluka = st.sidebar.multiselect("Select Taluka:", options= df_selection1['Taluka Name'].unique(),default= df_selection1['Taluka Name'].unique())
    df_selection=df_selection1[(df_selection1['Taluka Name'].isin(taluka))]

    xyz = df_selection[['Year', "Total Applications"]]
    fig1 = px.bar(xyz, x='Year', y='Total Applications', title="<b>Total Applications per Year<b>", text_auto=True)
    fig1.update_layout(
        plot_bgcolor='#E6D5B8',
        paper_bgcolor='#D4B996',
        font=dict(color='black', size=14),
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Total Applications", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20,
    )
    st.plotly_chart(fig1)
    st.markdown(xyz.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #2
    x_farmers=df_selection[['Year','Farmers']]
    x_farmers['Farmers']=x_farmers['Farmers'].astype("int64")
    fig2=px.bar(x_farmers,x='Year',y='Farmers',title="<b>Total Farmers per Year<b>",text_auto=True,color_discrete_sequence=["#ff7f0e"])
    fig2.update_layout(
        plot_bgcolor='#B2EBF2',  # Inside plot area
        paper_bgcolor='#f0f2f6',  # Outside chart area
        font=dict(
            color='black',  # Keep general text black
            size=14  # Optional: Adjust font size
        ),
        xaxis=dict(
            title=dict(text="Year", font=dict(color='red'))  # X-axis label in red
        ),
        yaxis=dict(
            title=dict(text="Farmers", font=dict(color='red'))  # Y-axis label in red
        ),  
        title_font_size=20,     # Optional: Change title font size
    )
    st.plotly_chart(fig2)
    st.markdown(x_farmers.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)

#3
    cluster_bar = df_selection[['Year', 'Total Applications', 'Farmers']]
    cluster_bar['Farmers']=cluster_bar['Farmers'].astype("int64")

    # Reshape data (Convert Wide to Long Format)
    xyz_melted = cluster_bar.melt(id_vars=['Year'], value_vars=['Total Applications', 'Farmers'], 
                                  var_name='Category', value_name='Count')
    
    # Create a Clustered Bar Chart
    fig3 = px.bar(
        xyz_melted, 
        x='Year', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Applications & Farmers per Year</b>", 
        text_auto=True,
        color_discrete_map={"Total Applications": "#1f77b4", "Farmers": "#ff7f0e"} 
    )
    fig3.update_layout(
        plot_bgcolor='#FFFAF0',  # Inside plot area
        paper_bgcolor='#FAEBD7',  # Outside chart area
        font=dict(
            color='black',  # Keep general text black
            size=14  # Optional: Adjust font size
        ),
        xaxis=dict(
            title=dict(text="Year", font=dict(color='red'))  # X-axis label in red
        ),
        yaxis=dict(
            title=dict(text="Count", font=dict(color='red'))  # Y-axis label in red
        ),
        
        title_font_size=20,     # Optional: Change title font size
    )
    
    # Display in Streamlit
    st.plotly_chart(fig3)
    st.markdown(cluster_bar.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)


    #4
    area_insured=df_selection[['Year','Area Insured (in thousand ha)']]
    area_insured['Area Insured (in thousand ha)'] =  area_insured['Area Insured (in thousand ha)'].round(1)
    area_insured['Area Insured (in thousand ha)'] =  area_insured['Area Insured (in thousand ha)'].astype("int64")
    fig4=px.bar(area_insured,x='Area Insured (in thousand ha)',y='Year',title="<b>Area Insured(in thousand ha) per Year<b>",text_auto=True,color_discrete_sequence=["#6a0dad"],orientation='h') 
    fig4.update_layout(
        plot_bgcolor='#F3F3F7',  # Light Lavender Gray inside the plot
        paper_bgcolor='#E6E6FA',  # Soft Lavender outside the chart
        font=dict(
            color='black',  # Keep general text black
            size=14  # Optional: Adjust font size
        ),
        xaxis=dict(
            title=dict(text="Area Insured(in thousand ha)", font=dict(color='red'))  # X-axis label in red
        ),
        yaxis=dict(
            title=dict(text="Year", font=dict(color='red'))  # Y-axis label in red
        ),
        title_font_size=20,
    )
    st.plotly_chart(fig4)
    st.markdown(area_insured.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #5
    gross_premium=df_selection[['Year','Gross Premium (in lakhs)']]
    gross_premium['Gross Premium (in lakhs)'] =  gross_premium['Gross Premium (in lakhs)'].round(1)
    gross_premium['Gross Premium (in lakhs)'] =  gross_premium['Gross Premium (in lakhs)'].astype("int64")
    fig5=px.bar(gross_premium,x='Year',y='Gross Premium (in lakhs)',title="<b>Gross Premium(in lakhs) per Year<b>",text_auto=True,color_discrete_sequence=["#e63946"]) 
    fig5.update_layout(
        plot_bgcolor='#1E1E1E',  # Dark Gray inside the plot
        paper_bgcolor='#2C2C2C',  # Blackish Gray outside the chart
        font=dict(color='white', size=14),
        xaxis=dict(title=dict(text="Year", font=dict(color='white'))),
        yaxis=dict(title=dict(text="Gross Premium (in lakhs)", font=dict(color='white'))),
        title=dict(
            text="<b>Gross Premium (in lakhs) per Year</b>",
            font=dict(color='white', size=20)  
        )
    ) 
    st.plotly_chart(fig5)
    st.markdown(gross_premium.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #6
    Line_chart = df_selection[['Year', 'Gross Premium/Sum insured']]
    Line_chart['Gross Premium/Sum insured']=(Line_chart['Gross Premium/Sum insured'].round(2))*100
    Line_chart['Gross Premium/Sum insured']=(Line_chart['Gross Premium/Sum insured'].astype("int64"))

    fig6 = px.line(Line_chart, x='Year', y='Gross Premium/Sum insured', 
                   title="<b>Gross Premium / Sum Insured per Year</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#2ca02c"])  # Green color
    fig6.update_traces(text=Line_chart['Gross Premium/Sum insured'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
    fig6.update_layout(
        plot_bgcolor='#D7CCC8',  # Warm Light Brown inside the plot
        paper_bgcolor='#A1887F',  # Deeper Earthy Brown outside the chart
        font=dict(color='black', size=14),
        xaxis=dict(title=dict(text="Year", font=dict(color='White')),tickfont=dict(color='white') 
        ),
        yaxis=dict(title=dict(text="Gross Premium\Sum insured", font=dict(color='White')) ,                	  	tickfont=dict(color='white')
        ),
        title_font_size=20
      
    )
    st.plotly_chart(fig6)
    Line_chart.rename(columns={'Gross Premium/Sum insured': 'Gross Premium/Sum insured (in %)'}, inplace=True)
    st.markdown(Line_chart.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #7
    sum_insured=df_selection[['Year','Sum Insured (in lakhs)']]
    sum_insured['Sum Insured (in lakhs)']=(sum_insured['Sum Insured (in lakhs)'].round(2))
    sum_insured['Sum Insured (in lakhs)']=(sum_insured['Sum Insured (in lakhs)'].astype("int64"))

    fig7=px.bar(sum_insured,x='Sum Insured (in lakhs)',y='Year',title="<b>Sum Insured (in lakhs) per Year<b>",text_auto=True,color_discrete_sequence=["#ff006e"],orientation='h')  
    fig7.update_layout(
        plot_bgcolor='#E3F2FD',  # Soft Blue inside the plot
        paper_bgcolor='#BBDEFB',  # Light Sky Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Sum Insured (in lakhs)", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
    st.plotly_chart(fig7)
    st.markdown(sum_insured.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #9
    Line_chart1 = df_selection[['Year', 'Total Claim/Gross Premium']]
    Line_chart1['Total Claim/Gross Premium']=(Line_chart1['Total Claim/Gross Premium'].round(2))*100
    Line_chart1['Total Claim/Gross Premium']=(Line_chart1['Total Claim/Gross Premium'].astype("int64"))
    fig9 = px.line(Line_chart1, x='Year', y='Total Claim/Gross Premium', 
                   title="<b>Total Claim/Gross Premium</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#4b5563"])  # Green color
    fig9.update_traces(text=Line_chart1['Total Claim/Gross Premium'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
    fig9.update_layout(
        plot_bgcolor='#F0F4C3',  # Light Sky Blue inside the plot
        paper_bgcolor='#C5E1A5',  # Soft Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Total Claim/Gross Premium", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    
    st.plotly_chart(fig9)
    Line_chart1.rename(columns={'Total Claim/Gross Premium': 'Total Claim/Gross Premium (in %)'}, inplace=True)
    st.markdown(Line_chart1.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #10
    cluster_bar2 = df_selection[['Year', 'Total Claim Paid (in lakhs)', 'Midterm and Localised and Post Harvest']]
    cluster_bar2['Total Claim Paid (in lakhs)']=cluster_bar2['Total Claim Paid (in lakhs)'].astype("int64")
    xyz_melted2 = cluster_bar2.melt(id_vars=['Year'], value_vars=['Midterm and Localised and Post Harvest', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig10 = px.bar(
        xyz_melted2, 
        x='Year', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim against Midterm and Localised and Post Harvest per Year</b>", 
        text_auto=True,
        color_discrete_map={"Total Claim Paid (in lakhs)": "#2ca02c", "Midterm and Localised and Post Harvest": "#4b5563 "}  # Blue & Orange
    )
    
    fig10.update_layout(
        plot_bgcolor='#E6D5B8',  # Warm Earthy inside the plot
        paper_bgcolor='#D4B996',  # Soft Brownish-Cream outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    st.plotly_chart(fig10)
    cluster_bar2.rename(columns={'Midterm and Localised and Post Harvest': 'Midterm and Localised and Post Harvest (in lakhs)'}, inplace=True)
    st.markdown(cluster_bar2.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)


    #11
    loss = df_selection[['Year', 'Total Revenue in Cr']].copy()
    
    # Add a new column to define colors dynamically
    loss['Color'] = np.where(loss['Total Revenue in Cr'] >= 0, 'green', 'red')
    
    # Create a bar chart with conditional colors
    fig11 = px.bar(
        loss,
        x='Year',
        y='Total Revenue in Cr',
        title="<b>Total Revenue in Cr per Year</b>",
        text_auto=True,
        color='Color',  # Use the dynamically assigned color column
        color_discrete_map={"green": "#2ca02c", "red": "#d62728"}  # Green for +ve, Red for -ve
    )
    fig11.update_layout(
        plot_bgcolor='#F9E5E5',  # Light Pink inside the plot
        paper_bgcolor='#E8C9C9',  # Soft Pastel Rose outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Total Revenue in Cr", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
    # Hide legend (since we are only using color for visual effect)
    fig11.update_layout(showlegend=False)
    
    # Display in Streamlit
    st.plotly_chart(fig11)


    #12
    cluster_bar3 = df_selection[['Year', 'Total Claim Paid (in lakhs)', 'Yield Based (in lakhs)']]
    cluster_bar3['Total Claim Paid (in lakhs)']=cluster_bar3['Total Claim Paid (in lakhs)'].astype("int64")
    cluster_bar3['Yield Based (in lakhs)']=cluster_bar3['Yield Based (in lakhs)'].astype("int64")
    xyz_melted3 = cluster_bar3.melt(id_vars=['Year'], value_vars=['Yield Based (in lakhs)', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig12 = px.bar(
        xyz_melted3, 
        x='Year', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim Paid (in lakhs) and Yield Based (in lakhs) per Year</b>", 
        text_auto=True,
        color_discrete_map={"Yield Based (in lakhs)": "#ffc107", "Total Claim Paid (in lakhs)": "#dc3545"}  # Blue & Orange
    )
    fig12.update_layout(
        plot_bgcolor='#FFF5E1',  # Light Peach inside the plot
        paper_bgcolor='#FFDFBA',  # Soft Orange outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    st.plotly_chart(fig12)
    st.markdown(cluster_bar3.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)
 

#13

    cluster_bar4 = df_selection[['Year', 'Total Claim Paid (in lakhs)', 'Gross Premium (in lakhs)']]
    cluster_bar4['Total Claim Paid (in lakhs)']=cluster_bar4['Total Claim Paid (in lakhs)'].astype("int64")
    cluster_bar4['Gross Premium (in lakhs)']=cluster_bar4['Gross Premium (in lakhs)'].astype("int64")




    xyz_melted4 = cluster_bar4.melt(id_vars=['Year'], value_vars=['Gross Premium (in lakhs)', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig13 = px.bar(
        xyz_melted4, 
        x='Year', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim Paid (in lakhs) and Gross Premium (in lakhs) per Year</b>", 
        text_auto=True,
        color_discrete_map={"Gross Premium (in lakhs)": "#32CD32", "Total Claim Paid (in lakhs)": "#4B0082"}  # Blue & Orange
    )
    fig13.update_layout(
        plot_bgcolor='#F0F8FF',  # Light Peach inside the plot
        paper_bgcolor='#B0E0E6',  # Soft Orange outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    st.plotly_chart(fig13)
    st.markdown(cluster_bar4.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)




       



def Taluka_Wise_Analysis():
    st.title("Taluka Wise Analysis PMFBY 2018-2023")
    st.sidebar.header("Taluka Wise Analysis")

    year = st.sidebar.selectbox("Select Year:", options=df['Year'].unique())
    district = st.sidebar.selectbox("Select District:", options=df[df['Year'] == year]['District Name'].unique())

    df_selection = df[(df['Year'] == year) & (df['District Name'] == district)]
#1
    cluster_bar = df_selection[['Taluka Name', 'Total Applications', 'Farmers']]
    cluster_bar['Farmers']=cluster_bar['Farmers'].astype("int64")
    xyz_melted = cluster_bar.melt(id_vars=['Taluka Name'], value_vars=['Total Applications', 'Farmers'], 
                                  var_name='Category', value_name='Count')
    fig1 = px.bar(
        xyz_melted, 
        x='Taluka Name', 
        y='Count', 
        color='Category',
        barmode='group',
        title="<b>Total Applications & Farmers per Taluka</b>", 
        text_auto=True,
        color_discrete_map={"Total Applications": "#1f77b4", "Farmers": "#ff7f0e"} 
    )
    fig1.update_layout(
        plot_bgcolor='#FFFAF0',
        paper_bgcolor='#FAEBD7',
        font=dict(
            color='black',
            size=14
        ),
        xaxis=dict(
            title=dict(text="Taluka Name", font=dict(color='red'))
        ),
        yaxis=dict(
            title=dict(text="Count", font=dict(color='red'))
        ),
        title_font_size=20,
    )
    st.plotly_chart(fig1)
    st.markdown(cluster_bar.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)

    #2
    area_insured=df_selection[['Taluka Name','Area Insured (in thousand ha)']]
    area_insured['Area Insured (in thousand ha)'] =  area_insured['Area Insured (in thousand ha)'].round(1)
    area_insured['Area Insured (in thousand ha)'] =  area_insured['Area Insured (in thousand ha)'].astype("int64")


    fig2=px.bar(area_insured,x='Area Insured (in thousand ha)',y='Taluka Name',title="<b>Area Insured (in thousand ha) Taluka Wise<b>",text_auto=True,color_discrete_sequence=["#6a0dad"],orientation='h')  
    fig2.update_layout(
        plot_bgcolor='#F3F3F7',  # Light Lavender Gray inside the plot
        paper_bgcolor='#E6E6FA',  # Soft Lavender outside the chart
        font=dict(
            color='black',  # Keep general text black
            size=14  # Optional: Adjust font size
        ),
        xaxis=dict(
            title=dict(text="Area Insured (in thousand ha)", font=dict(color='red'))  # X-axis label in red
        ),
        yaxis=dict(
            title=dict(text="Taluka Name", font=dict(color='red'))  # Y-axis label in red
        ),
        title_font_size=20
    )
    st.plotly_chart(fig2)
    st.markdown(area_insured.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)




    #3
    gross_premium=df_selection[['Taluka Name','Gross Premium (in lakhs)']]
    gross_premium['Gross Premium (in lakhs)'] =  gross_premium['Gross Premium (in lakhs)'].round(1)
    gross_premium['Gross Premium (in lakhs)'] =  gross_premium['Gross Premium (in lakhs)'].astype("int64")
    fig3=px.bar(gross_premium,x='Taluka Name',y='Gross Premium (in lakhs)',title="<b>Gross Premium(in lakhs) Taluka Wise<b>",text_auto=True,color_discrete_sequence=["#e63946"])  
    fig3.update_layout(
        plot_bgcolor='#1E1E1E',  # Dark Gray inside the plot
        paper_bgcolor='#2C2C2C',  # Blackish Gray outside the chart
        font=dict(color='white', size=14),
        xaxis=dict(title=dict(text="Taluka Name", font=dict(color='white'))),
        yaxis=dict(title=dict(text="Gross Premium (in lakhs)", font=dict(color='white'))),
        title=dict(
            text="<b>Gross Premium (in lakhs) Taluka Wise</b>",
            font=dict(color='white', size=20)  
        )
    ) 
    
    st.plotly_chart(fig3)
    st.markdown(gross_premium.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)


     #4
    Line_chart = df_selection[['Taluka Name', 'Gross Premium/Sum insured']]
    Line_chart['Gross Premium/Sum insured']=(Line_chart['Gross Premium/Sum insured'].round(2))*100
    Line_chart['Gross Premium/Sum insured']=(Line_chart['Gross Premium/Sum insured'].astype("int64"))
    fig4 = px.line(Line_chart, x='Taluka Name', y='Gross Premium/Sum insured', 
                   title="<b>Gross Premium / Sum Insured Taluka Wise</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#2ca02c"])  # Green color
    fig4.update_traces(text=Line_chart['Gross Premium/Sum insured'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
    fig4.update_layout(
        plot_bgcolor='#D7CCC8',  # Warm Light Brown inside the plot
        paper_bgcolor='#A1887F',  # Deeper Earthy Brown outside the chart
        font=dict(color='black', size=14),
        xaxis=dict(title=dict(text="Taluka Name", font=dict(color='White')),tickfont=dict(color='white') 
        ),
        yaxis=dict(title=dict(text="Gross Premium\Sum insured", font=dict(color='White')) ,tickfont=dict(color='white')
        ),
        title_font_size=20
      
    )
    
    
    st.plotly_chart(fig4)
    Line_chart.rename(columns={'Gross Premium/Sum insured': 'Gross Premium/Sum insured (in %)'}, inplace=True)
    st.markdown(Line_chart.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)


    #5
    sum_insured=df_selection[['Taluka Name','Sum Insured (in lakhs)']]
    sum_insured['Sum Insured (in lakhs)']=(sum_insured['Sum Insured (in lakhs)'].round(2))
    sum_insured['Sum Insured (in lakhs)']=(sum_insured['Sum Insured (in lakhs)'].astype("int64"))

    fig5=px.bar(sum_insured,x='Sum Insured (in lakhs)',y='Taluka Name',title="<b>Sum Insured (In Lac.) Taluka Wise<b>",text_auto=True,color_discrete_sequence=["#ff006e"],orientation='h')
    fig5.update_layout(
        plot_bgcolor='#E3F2FD',  # Soft Blue inside the plot
        paper_bgcolor='#BBDEFB',  # Light Sky Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Sum Insured (in lakhs)", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Taluka Name", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
      
    st.plotly_chart(fig5)
    st.markdown(sum_insured.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #7
    Line_chart1 = df_selection[['Taluka Name', 'Total Claim/Gross Premium']]
    Line_chart1['Total Claim/Gross Premium']=(Line_chart1['Total Claim/Gross Premium'].round(2))*100
    Line_chart1['Total Claim/Gross Premium']=(Line_chart1['Total Claim/Gross Premium'].astype("int64"))
    fig7 = px.line(Line_chart1, x='Taluka Name', y='Total Claim/Gross Premium', 
                   title="<b>Claim/ Gross Premium</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#adb5bd"])  # Green color
    fig7.update_traces(text=Line_chart1['Total Claim/Gross Premium'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
    fig7.update_layout(
        plot_bgcolor='#E3F2FD',  # Light Sky Blue inside the plot
        paper_bgcolor='#BBDEFB',  # Soft Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Taluka Name", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Total Claim/Gross Premium", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    st.plotly_chart(fig7)
    Line_chart1.rename(columns={'Total Claim/Gross Premium': 'Total Claim/Gross Premium (in %)'}, inplace=True)
    st.markdown(Line_chart1.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)



    #8
    cluster_bar2 = df_selection[['Taluka Name', 'Total Claim Paid (in lakhs)', 'Midterm and Localised and Post Harvest']]
    cluster_bar2['Total Claim Paid (in lakhs)']=cluster_bar2['Total Claim Paid (in lakhs)'].astype("int64")

    xyz_melted2 = cluster_bar2.melt(id_vars=['Taluka Name'], value_vars=['Midterm and Localised and Post Harvest', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig8 = px.bar(
        xyz_melted2, 
        x='Taluka Name', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Total Claim against Midterm and Localised and Post Harvest Taluka Wise</b>", 
        text_auto=True,
        color_discrete_map={"Total Claim Paid (in lakhs)": "#2ca02c", "Midterm and Localised and Post Harvest": "#4b5563 "}  # Blue & Orange
    )
    fig8.update_layout(
        plot_bgcolor='#E6D5B8',  # Warm Earthy inside the plot
        paper_bgcolor='#D4B996',  # Soft Brownish-Cream outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Taluka Name", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    
    st.plotly_chart(fig8)
    cluster_bar2.rename(columns={'Midterm and Localised and Post Harvest': 'Midterm and Localised and Post Harvest (in lakhs)'}, inplace=True)
    st.markdown(cluster_bar2.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)

    
    
    
    #9
    loss = df_selection[['Taluka Name', 'Total Revenue in Cr']].copy()
    
    # Add a new column to define colors dynamically
    loss['Color'] = np.where(loss['Total Revenue in Cr'] >= 0, 'green', 'red')
    
    # Create a bar chart with conditional colors
    fig9 = px.bar(
        loss,
        x='Taluka Name',
        y='Total Revenue in Cr',
        title="<b>Total Revenue Taluka Wise</b>",
        text_auto=True,
        color='Color',  # Use the dynamically assigned color column
        color_discrete_map={"green": "#2ca02c", "red": "#d62728"}  # Green for +ve, Red for -ve
    )
    fig9.update_layout(
        plot_bgcolor='#F0F4C3',  # Light Pink inside the plot
        paper_bgcolor='#C5E1A5',  # Soft Pastel Rose outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Taluka Name", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Total Revenue in Cr", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
    
    
    # Hide legend (since we are only using color for visual effect)
    fig9.update_layout(showlegend=False)
    
    # Display in Streamlit
    st.plotly_chart(fig9)
    
    
    #10
    cluster_bar3 = df_selection[['Taluka Name', 'Total Claim Paid (in lakhs)', 'Yield Based (in lakhs)']]
    cluster_bar3['Total Claim Paid (in lakhs)']=cluster_bar3['Total Claim Paid (in lakhs)'].astype("int64")
    cluster_bar3['Yield Based (in lakhs)']=cluster_bar3['Yield Based (in lakhs)'].astype("int64")

    xyz_melted3 = cluster_bar3.melt(id_vars=['Taluka Name'], value_vars=['Yield Based (in lakhs)', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig10 = px.bar(
        xyz_melted3, 
        x='Taluka Name', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim Paid (in lakhs) and Yield Based (in lakhs) Taluka Wise</b>", 
        text_auto=True,
        color_discrete_map={"Yield Based (in lakhs)": "#ffc107", "Total Claim Paid (in lakhs)": "#dc3545"}  # Blue & Orange
    )
    fig10.update_layout(
        plot_bgcolor='#FFF5E1',  # Light Peach inside the plot
        paper_bgcolor='#FFDFBA',  # Soft Orange outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Taluka Name", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    
    st.plotly_chart(fig10)
    st.markdown(cluster_bar3.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)


#11
    cluster_bar4 = df_selection[['Taluka Name', 'Total Claim Paid (in lakhs)', 'Gross Premium (in lakhs)']]
    cluster_bar4['Total Claim Paid (in lakhs)']=cluster_bar4['Total Claim Paid (in lakhs)'].astype("int64")
    cluster_bar4['Gross Premium (in lakhs)']=cluster_bar4['Gross Premium (in lakhs)'].astype("int64")




    xyz_melted4 = cluster_bar4.melt(id_vars=['Taluka Name'], value_vars=['Gross Premium (in lakhs)', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig11 = px.bar(
        xyz_melted4, 
        x='Taluka Name', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim Paid (in lakhs) and Gross Premium (in lakhs)</b>", 
        text_auto=True,
        color_discrete_map={"Gross Premium (in lakhs)": "#32CD32", "Total Claim Paid (in lakhs)": "#4B0082"}  # Blue & Orange
    )
    fig11.update_layout(
        plot_bgcolor='#F0F8FF',  # Light Peach inside the plot
        paper_bgcolor='#B0E0E6',  # Soft Orange outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Taluka Name", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    st.plotly_chart(fig11)
    st.markdown(cluster_bar4.style.hide(axis='index').set_table_attributes("class='dataframe' style='width: 80%; border: 1px solid #0D47A1; border-radius: 8px;' ").set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#0D47A1'), ('color', 'white'), ('text-align', 'center'), ('font-size', '16px'), ('padding', '6px')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '14px'), ('padding', '6px')]}])
    .to_html(), unsafe_allow_html=True)




    
page=st.sidebar.selectbox('Select Analysis',['header_page','Year_Wise_Analysis','Taluka_Wise_Analysis'])
if page == 'Year_Wise_Analysis':
    Year_Wise_Analysis()
elif page == 'Taluka_Wise_Analysis':
    Taluka_Wise_Analysis()
else:
    header_page()
