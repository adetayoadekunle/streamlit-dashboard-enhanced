import streamlit as st
import pandas as pd

st.header("School Learning Modalities Dashboard")
st.subheader("Looking at data and visuals")

st.text("The dashboard will look NCES school learning modalities data in 2020-2021.")

# ## https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000") ## first 1k 

## data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

df['week'].value_counts()


## box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts/schools:", df['district_name'].nunique())

## exposing first 1k of NCES 20-21 data
st.dataframe(df)



table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()
table.columns

## line chart by week 
st.bar_chart(
    table,
    x="week",
    y="Hybrid",
)

st.bar_chart(
    table,
    x="week",
    y="In Person",
)

st.bar_chart(
    table,
    x="week",
    y="Remote",
)

# Filter Data by ZIP Code
st.markdown("### Filter Data by ZIP Code")
unique_zips = sorted(df['zip_code'].unique())  
selected_zip = st.selectbox("Select a ZIP Code", unique_zips)  
zip_filtered_df = df[df['zip_code'] == selected_zip]  

# Display the Filtered Data
st.markdown(f"### Data for ZIP Code: {selected_zip}")
st.dataframe(zip_filtered_df)

# Descriptive summary
st.markdown("### Data Overview")
total_students = df['student_count'].sum()
total_weeks = df['week_recoded'].nunique()
total_zip_codes = df['zip_code'].nunique()

# Show total students, weeks, and unique zip codes
st.write(f"**Total Students:** {total_students}")
st.write(f"**Total Weeks of Data:** {total_weeks}")
st.write(f"**Total Unique ZIP Codes:** {total_zip_codes}")

# Bar chart for total students each week
st.markdown("### Total Students Per Week")
students_per_week = df.groupby('week_recoded')['student_count'].sum()

st.bar_chart(students_per_week)

# Average Students Per District
st.markdown("### Average Students Per District")
average_students = df.groupby('district_name')['student_count'].mean().mean()
st.write(f"**Average Students Per District:** {average_students:.2f}")
