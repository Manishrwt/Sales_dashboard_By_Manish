import streamlit as st
import pandas as pd
import plotly.express as px
import os
import plotly.figure_factory as ff
import warnings

warnings.filterwarnings('ignore')

# Set up the page configuration
st.set_page_config(page_title="Sales Dashboard By Manish", page_icon="🛒", layout="wide")

# Function to apply custom styles with colorful backgrounds
def add_custom_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f6;  /* Light background color */
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2b547e;  /* Heading color */
        }
        .stSidebar {
            background-color: #d1e0f7;  /* Sidebar background color */
            color: #333333;  /* Sidebar text color */
        }
        .css-18e3th9 {  /* Main content text color */
            color: #2b547e;  /* Set text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply the custom styles
add_custom_style()

# Title and styling
st.markdown("<br><br>", unsafe_allow_html=True) 
st.title(" 🛒 SALES DASHBOARD BY MANISH ")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# File uploader or load default data
file = st.file_uploader(":file_folder: Upload your file", type=(["csv", "xlsx", "xls", "txt"]))

if file is not None:
    df = pd.read_csv(file, encoding="ISO-8859-1")
else:
    # Set default path to Indian dataset
    os.chdir(r"C:/Users/manis/OneDrive/Desktop/Streamlit_Project")
    df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")  # Make sure your dataset has Indian states/cities

# Convert 'Order Date' column to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Sidebar filters for date range, Indian states, cities, and regions
st.sidebar.header("Choose your filter:")

# Set date filters
col1, col2 = st.columns((2))
startDate = df['Order Date'].min()
endDate = df['Order Date'].max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)]

# Predefined list of Indian regions, states, and cities
indian_regions = ["North", "South", "East", "West", "Central"]
indian_states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
    'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
    'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
    'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
    'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi', 'Jammu and Kashmir']

indian_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai', 
    'Kolkata', 'Pune', 'Jaipur', 'Lucknow', 'Surat', 'Kanpur', 
    'Nagpur', 'Visakhapatnam', 'Patna', 'Bhopal', 'Indore', 
    'Vadodara', 'Coimbatore', 'Madurai', 'Thane']

# Sidebar filters for Indian regions, states, and cities
region = st.sidebar.multiselect("Select Region:", indian_regions)
if not region:
    filtered_df = df
else:
    # Assuming that the dataset has a column 'Region' that contains the respective regions
    filtered_df = df[df["Region"].isin(region)]

state = st.sidebar.multiselect("Select State:", indian_states)
if not state:
    filtered_df = filtered_df
else:
    filtered_df = filtered_df[filtered_df["State"].isin(state)]

city = st.sidebar.multiselect("Select City:", indian_cities)
if not city:
    filtered_df = filtered_df
else:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

if page == "Home":
    # Category-wise Sales bar chart
    category_df = filtered_df.groupby("Category").agg({"Sales": "sum"}).reset_index()
    st.subheader("Category-wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales", text=[f"${x:,.2f}" for x in category_df["Sales"]], template="seaborn")
    st.plotly_chart(fig, use_container_width=True)

    # State-wise Sales pie chart
    st.subheader("State-wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="State", hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Download filtered data
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data", data=csv, file_name="filtered_data.csv", mime="text/csv")

    # Time series analysis of sales
    st.subheader("Time Series Analysis of Sales")
    filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M").astype(str)  # Convert to string to avoid serialization issues
    sales_ts = filtered_df.groupby("month_year")["Sales"].sum().reset_index()
    fig = px.line(sales_ts, x="month_year", y="Sales", labels={"Sales": "Amount"}, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Hierarchical view of Sales using TreeMap
    st.subheader("Hierarchical View of Sales by State, Category, Sub-Category")
    fig = px.treemap(filtered_df, path=["State", "Category", "Sub-Category"], values="Sales", hover_data=["Sales"], color="Sub-Category")
    st.plotly_chart(fig, use_container_width=True)

    # Scatter plot of Sales vs Profit
    st.subheader("Relationship between Sales and Profits")
    scatter_fig = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity", color="Category", hover_data=["Sub-Category"])
    st.plotly_chart(scatter_fig, use_container_width=True)

    # Pivot table for Sub-Category sales by month
    st.subheader("Sub-Category Sales by Month")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_cat_pivot = pd.pivot_table(filtered_df, values="Sales", index="Sub-Category", columns="month", aggfunc="sum")
    st.write(sub_cat_pivot.style.background_gradient(cmap="Blues"))

    # Download original dataset
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Original Dataset", data=csv, file_name="Indian_Superstore.csv", mime="text/csv")

elif page == "About":
    st.subheader("About Me")
    st.write("**Name**: Manish Rawat")
    st.write("**Institution**: VIT Vellore")
    st.write("**Program**: M.Tech in AI & ML")
    st.write("**Registration Number**: 24MAI0113")

elif page == "Contact":
    st.subheader("Contact Information")
    st.write("For more information, please reach out via email or phone.")
    st.write("**Email**: manish2018rewa@gmail.com")
    st.write("**Phone**: 6263377546")
    st.markdown("""  
        **Social Media Links**:  
        [![YouTube](https://img.icons8.com/color/48/000000/youtube--v1.png)](https://www.youtube.com/@mnishrwat4314)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [![Instagram](https://img.icons8.com/color/48/000000/instagram-new.png)](https://www.instagram.com/manish___rwt?igsh=ZjlpZmFqc2p1NmU4)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [![LinkedIn](https://img.icons8.com/color/48/000000/linkedin.png)](https://linkedin.com)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [![GitHub](https://img.icons8.com/color/48/000000/github--v1.png)](https://github.com/Manishrwt)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    """, unsafe_allow_html=True)
