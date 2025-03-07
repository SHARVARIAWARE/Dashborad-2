import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="PMBFY Claim Analysis",layout="wide")
st.markdown(
    """
    <style>
        /* Change the entire page background */
        .stApp {
            background-color: #e6f2ff; /* Light Blue */
        }
        
        /* Change sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #d3e0ea; /* Light Grayish Blue */
        }

        /* Change main content area */
        .block-container {
            background-color: #ffffff; /* White */
            padding: 20px;
            border-radius: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
def header_page():
    st.markdown("<h1 style='text-align: center,color: black;'>PMFBY Analysis 2018-2023</h1>",unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center,color: black;'Sharvari Aware</h2>",unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center,color: black;'>Data Science Intern</h3>",unsafe_allow_html=True)
f1=st.file_uploader(":file_folder:Upload a file",type=['xlsx','xls'])
if f1 is not None:
    filename=f1.name
    st.write(filename)

    df=pd.read_excel(f1,engine="openpyxl")
else:
    st.markdown("Please upload a file")

def Year_Wise_Analysis():
    st.title("Year  Wise Analysis PMFBY 2018-2023")
    st.sidebar.header("Select the District:")
    district=st.sidebar.multiselect("Select the District:",options=df['District Name'].unique(),default=df['District Name'].unique())
    df_selection = df[(df['District Name'].isin(district)) ]
    #1
    xyz=df_selection[['Year',"Total Applications"]]
    fig1=px.bar(xyz,x='Year',y='Total Applications',title="<b>Total Applications per Year<b>",text_auto=True)
    fig1.update_layout(
        plot_bgcolor='#E6D5B8',  # Warm Earthy inside the plot
        paper_bgcolor='#D4B996',  # Soft Brownish-Cream outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Total Applications", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20,     # Optional: Change title font size
    )
    st.plotly_chart(fig1)

       #2
    x_farmers=df_selection[['Year','Farmers']]
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
        
    
    #3
    cluster_bar = df_selection[['Year', 'Total Applications', 'Farmers']]
    
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
       
    
    
    
    #4
    area_insured=df_selection[['Year','Area Insured (in thousand ha)']]
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
       
    
    
    
    #5
    gross_premium=df_selection[['Year','Gross Premium (in lakhs)']]
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
        
    
    
    
    
    
    #6
    Line_chart = df_selection[['Year', 'Premium\Sum insured']]
    fig6 = px.line(Line_chart, x='Year', y='Premium\Sum insured', 
                   title="<b>Gross Premium / Sum Insured per Year</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#2ca02c"])  # Green color
    fig6.update_traces(text=Line_chart['Premium\Sum insured'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
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
       
    
    
    #7
    sum_insured=df_selection[['Year','Sum Insured (In Lac.)']]
    fig7=px.bar(sum_insured,x='Sum Insured (In Lac.)',y='Year',title="<b>Sum Insured (In Lac.) per Year<b>",text_auto=True,color_discrete_sequence=["#ff006e"],orientation='h')  
    fig7.update_layout(
        plot_bgcolor='#E3F2FD',  # Soft Blue inside the plot
        paper_bgcolor='#BBDEFB',  # Light Sky Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Sum Insured (In Lac.)", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
    st.plotly_chart(fig7)
       
    
    
    
    
    
    
    #9
    Line_chart1 = df_selection[['Year', 'Claim\Premium']]
    fig9 = px.line(Line_chart1, x='Year', y='Claim\Premium', 
                   title="<b>Claim/ Gross Premium</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#4b5563"])  # Green color
    fig9.update_traces(text=Line_chart1['Claim\Premium'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
    fig9.update_layout(
        plot_bgcolor='#E3F2FD',  # Light Sky Blue inside the plot
        paper_bgcolor='#BBDEFB',  # Soft Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Claim/ Gross Premium", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    
    st.plotly_chart(fig9)
        
    
    
    
    
    
    #10
    cluster_bar2 = df_selection[['Year', 'Total Claim Paid (in lakhs)', 'MSA and ILA andPost Harvest']]
    xyz_melted2 = cluster_bar2.melt(id_vars=['Year'], value_vars=['MSA and ILA andPost Harvest', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig10 = px.bar(
        xyz_melted2, 
        x='Year', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim against MSA,ILA,Post Harvest per Year</b>", 
        text_auto=True,
        color_discrete_map={"Total Claim Paid (in lakhs)": "#2ca02c", "MSA and ILA andPost Harvest": "#4b5563 "}  # Blue & Orange
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
        
    
    
    
    
    #11
    loss = df_selection[['Year', 'Loss in Cr']].copy()
    
    # Add a new column to define colors dynamically
    loss['Color'] = np.where(loss['Loss in Cr'] >= 0, 'green', 'red')
    
    # Create a bar chart with conditional colors
    fig11 = px.bar(
        loss,
        x='Year',
        y='Loss in Cr',
        title="<b>Revenue per Year</b>",
        text_auto=True,
        color='Color',  # Use the dynamically assigned color column
        color_discrete_map={"green": "#2ca02c", "red": "#d62728"}  # Green for +ve, Red for -ve
    )
    fig11.update_layout(
        plot_bgcolor='#F9E5E5',  # Light Pink inside the plot
        paper_bgcolor='#E8C9C9',  # Soft Pastel Rose outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Loss in Cr", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
    # Hide legend (since we are only using color for visual effect)
    fig11.update_layout(showlegend=False)
    
    # Display in Streamlit
    st.plotly_chart(fig11)
        
    
    
    
    
    #12
    cluster_bar3 = df_selection[['Year', 'Total Claim Paid (in lakhs)', 'Yield Based (in lakhs)']]
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
    

def District_Wise_Analysis():
    st.title("District wise PMFBY Analysis 2018-2023")
    st.sidebar.header("Select the District:")
    year=st.sidebar.multiselect("Select the Year:",options=df['Year'].unique(),default=df['Year'].unique())
    
    df_selection = df[(df['Year'].isin(year)) ]
    
    #1
    cluster_bar = df_selection[['District Name', 'Total Applications', 'Farmers']]
    xyz_melted = cluster_bar.melt(id_vars=['District Name'], value_vars=['Total Applications', 'Farmers'], 
                                  var_name='Category', value_name='Count')
    fig1 = px.bar(
        xyz_melted, 
        x='District Name', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Applications & Farmers per Year</b>", 
        text_auto=True,
        color_discrete_map={"Total Applications": "#1f77b4", "Farmers": "#ff7f0e"} 
    )
    fig1.update_layout(
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
    st.plotly_chart(fig1)
    
    
    
    #2
    area_insured=df_selection[['District Name','Area Insured (in thousand ha)']]
    fig2=px.bar(area_insured,x='Area Insured (in thousand ha)',y='District Name',title="<b>Area Insured(in thousand ha) District Wise<b>",text_auto=True,color_discrete_sequence=["#6a0dad"],orientation='h')  
    fig2.update_layout(
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
        title_font_size=20
    )
    st.plotly_chart(fig2)
    
    
    #3
    gross_premium=df_selection[['District Name','Gross Premium (in lakhs)']]
    fig3=px.bar(gross_premium,x='District Name',y='Gross Premium (in lakhs)',title="<b>Gross Premium(in lakhs) District Wise<b>",text_auto=True,color_discrete_sequence=["#e63946"])  
    fig3.update_layout(
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
    
    st.plotly_chart(fig3)
    
    #4
    Line_chart = df_selection[['District Name', 'Premium\Sum insured']]
    fig4 = px.line(Line_chart, x='District Name', y='Premium\Sum insured', 
                   title="<b>Gross Premium / Sum Insured District Wise</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#2ca02c"])  # Green color
    fig4.update_traces(text=Line_chart['Premium\Sum insured'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
    fig4.update_layout(
        plot_bgcolor='#D7CCC8',  # Warm Light Brown inside the plot
        paper_bgcolor='#A1887F',  # Deeper Earthy Brown outside the chart
        font=dict(color='black', size=14),
        xaxis=dict(title=dict(text="Year", font=dict(color='White')),tickfont=dict(color='white') 
        ),
        yaxis=dict(title=dict(text="Gross Premium\Sum insured", font=dict(color='White')) ,                	  	tickfont=dict(color='white')
        ),
        title_font_size=20
      
    )
    
    
    st.plotly_chart(fig4)
    
    
    
    
    #5
    sum_insured=df_selection[['District Name','Sum Insured (In Lac.)']]
    fig5=px.bar(sum_insured,x='Sum Insured (In Lac.)',y='District Name',title="<b>Sum Insured (In Lac.) District Wise<b>",text_auto=True,color_discrete_sequence=["#ff006e"],orientation='h')
    fig5.update_layout(
        plot_bgcolor='#E3F2FD',  # Soft Blue inside the plot
        paper_bgcolor='#BBDEFB',  # Light Sky Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Sum Insured (In Lac.)", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
      
    st.plotly_chart(fig5)
    
    
    
    
    #7
    Line_chart1 = df_selection[['District Name', 'Claim\Premium']]
    fig7 = px.line(Line_chart1, x='District Name', y='Claim\Premium', 
                   title="<b>Claim/ Gross Premium</b>", 
                   markers=True,  # Adds points to the line
                   color_discrete_sequence=["#adb5bd"])  # Green color
    fig7.update_traces(text=Line_chart1['Claim\Premium'].round(2).astype(str), textposition="top center",mode="lines+markers+text")
    fig7.update_layout(
        plot_bgcolor='#E3F2FD',  # Light Sky Blue inside the plot
        paper_bgcolor='#BBDEFB',  # Soft Blue outside the chart
        font=dict(color='black', size=14),
        
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Claim/ Gross Premium", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    st.plotly_chart(fig7)
    
    
    
    
    
    #8
    cluster_bar2 = df_selection[['District Name', 'Total Claim Paid (in lakhs)', 'MSA and ILA andPost Harvest']]
    xyz_melted2 = cluster_bar2.melt(id_vars=['District Name'], value_vars=['MSA and ILA andPost Harvest', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig8 = px.bar(
        xyz_melted2, 
        x='District Name', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim against MSA,ILA,Post Harvest District Wise</b>", 
        text_auto=True,
        color_discrete_map={"Total Claim Paid (in lakhs)": "#2ca02c", "MSA and ILA andPost Harvest": "#4b5563 "}  # Blue & Orange
    )
    fig8.update_layout(
        plot_bgcolor='#E6D5B8',  # Warm Earthy inside the plot
        paper_bgcolor='#D4B996',  # Soft Brownish-Cream outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    
    st.plotly_chart(fig8)
    
    
    
    #9
    loss = df_selection[['District Name', 'Loss in Cr']].copy()
    
    # Add a new column to define colors dynamically
    loss['Color'] = np.where(loss['Loss in Cr'] >= 0, 'green', 'red')
    
    # Create a bar chart with conditional colors
    fig9 = px.bar(
        loss,
        x='District Name',
        y='Loss in Cr',
        title="<b>Revenue District Wise</b>",
        text_auto=True,
        color='Color',  # Use the dynamically assigned color column
        color_discrete_map={"green": "#2ca02c", "red": "#d62728"}  # Green for +ve, Red for -ve
    )
    fig9.update_layout(
        plot_bgcolor='#F9E5E5',  # Light Pink inside the plot
        paper_bgcolor='#E8C9C9',  # Soft Pastel Rose outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="Year", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Loss in Cr", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    )
    
    
    # Hide legend (since we are only using color for visual effect)
    fig9.update_layout(showlegend=False)
    
    # Display in Streamlit
    st.plotly_chart(fig9)
    
    
    #10
    cluster_bar3 = df_selection[['District Name', 'Total Claim Paid (in lakhs)', 'Yield Based (in lakhs)']]
    xyz_melted3 = cluster_bar3.melt(id_vars=['District Name'], value_vars=['Yield Based (in lakhs)', 'Total Claim Paid (in lakhs)'], 
                                  var_name='Category', value_name='Count')
    fig10 = px.bar(
        xyz_melted3, 
        x='District Name', 
        y='Count', 
        color='Category',  # Groups by 'Total Applications' and 'Farmers'
        barmode='group',  # Enables clustered bars
        title="<b>Total Claim Paid (in lakhs) and Yield Based (in lakhs) District Wise</b>", 
        text_auto=True,
        color_discrete_map={"Yield Based (in lakhs)": "#ffc107", "Total Claim Paid (in lakhs)": "#dc3545"}  # Blue & Orange
    )
    fig10.update_layout(
        plot_bgcolor='#FFF5E1',  # Light Peach inside the plot
        paper_bgcolor='#FFDFBA',  # Soft Orange outside the chart
        font=dict(color='black', size=14),
    
        xaxis=dict(title=dict(text="District Name", font=dict(color='black')), tickfont=dict(color='black')),
        yaxis=dict(title=dict(text="Count", font=dict(color='black')), tickfont=dict(color='black')),
        title_font_size=20
    
    )
    
    st.plotly_chart(fig10)
page=st.sidebar.selectbox('Select Analysis',['header_page','Year_Wise_Analysis','District_Wise_Analysis'])
if page == 'Year_Wise_Analysis':
    Year_Wise_Analysis()
elif page == 'District_Wise_Analysis':
    District_Wise_Analysis()
else:
    header_page()
