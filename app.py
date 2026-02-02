import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# title and basic setup
st.title("Data Cleaning and Analysis Project")
st.write("Mini Project - Pandas Data Cleaning and Analysis")

# file upload
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # read the data
    df = pd.read_csv(uploaded_file)
    
    st.subheader("1. Original Data")
    st.write(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    st.dataframe(df)
    
    # data info
    st.subheader("2. Data Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Types:**")
        st.write(df.dtypes)
    
    with col2:
        st.write("**Missing Values:**")
        missing = df.isnull().sum()
        st.write(missing[missing > 0])
    
    st.write("**Basic Statistics:**")
    st.write(df.describe())
    
    # data cleaning section
    st.subheader("3. Data Cleaning")
    
    # show duplicates
    duplicates = df.duplicated().sum()
    st.write(f"Duplicate rows found: {duplicates}")
    
    if st.button("Remove Duplicates"):
        df = df.drop_duplicates()
        st.success(f"Removed {duplicates} duplicate rows")
    
    # handle missing values
    st.write("**Handle Missing Values:**")
    strategy = st.selectbox("Select strategy:", 
                           ["None", "Drop rows with missing values", 
                            "Fill with mean", "Fill with median"])
    
    if strategy != "None":
        if st.button("Apply Missing Value Strategy"):
            if strategy == "Drop rows with missing values":
                df = df.dropna()
                st.success("Dropped rows with missing values")
            elif strategy == "Fill with mean":
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[col].fillna(df[col].mean(), inplace=True)
                st.success("Filled missing values with mean")
            elif strategy == "Fill with median":
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[col].fillna(df[col].median(), inplace=True)
                st.success("Filled missing values with median")
    
    # analysis section
    st.subheader("4. Data Analysis")
    
    # select column for analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select column for analysis:", numeric_cols)
        
        # calculate statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mean", f"{df[selected_col].mean():.2f}")
            st.metric("Median", f"{df[selected_col].median():.2f}")
        
        with col2:
            st.metric("Min", f"{df[selected_col].min():.2f}")
            st.metric("Max", f"{df[selected_col].max():.2f}")
        
        with col3:
            st.metric("Std Dev", f"{df[selected_col].std():.2f}")
            st.metric("Count", len(df[selected_col]))
        
        # correlation matrix
        if len(numeric_cols) > 1:
            st.write("**Correlation Matrix:**")
            corr = df[numeric_cols].corr()
            st.dataframe(corr)
    
    # visualization section
    st.subheader("5. Visualizations")
    
    viz_type = st.selectbox("Select visualization:", 
                           ["Histogram", "Box Plot", "Bar Chart"])
    
    if viz_type == "Histogram":
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column:", numeric_cols, key="hist")
            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=20, edgecolor='black')
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Histogram of {col}")
            st.pyplot(fig)
    
    elif viz_type == "Box Plot":
        if len(numeric_cols) > 0:
            cols = st.multiselect("Select columns:", numeric_cols, default=numeric_cols[:2])
            if cols:
                fig, ax = plt.subplots()
                df[cols].boxplot(ax=ax)
                ax.set_ylabel("Values")
                ax.set_title("Box Plot")
                st.pyplot(fig)
    
    elif viz_type == "Bar Chart":
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        if len(cat_cols) > 0:
            col = st.selectbox("Select column:", cat_cols, key="bar")
            value_counts = df[col].value_counts().head(10)
            fig, ax = plt.subplots()
            value_counts.plot(kind='bar', ax=ax)
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            ax.set_title(f"Bar Chart of {col}")
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    # cleaned data display
    st.subheader("6. Cleaned Data")
    st.write(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
    st.dataframe(df)
    
    # download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Cleaned Data",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file to begin analysis")
    
    # sample data button
    if st.button("Load Sample Data"):
        # create sample dataset
        sample_data = {
            'Student_ID': [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10],
            'Name': ['John', 'Mary', 'Bob', 'Alice', 'Tom', 'Tom', 'Jane', 'Mike', 'Sara', 'Paul', 'Emma'],
            'Age': [20, 21, 19, 22, 20, 20, None, 21, 19, 23, 20],
            'Math_Score': [85, 92, 78, 88, 95, 95, 82, None, 76, 84, 91],
            'Science_Score': [78, 88, 82, 91, 89, 89, 85, 93, 79, 87, 90],
            'Attendance': [95.5, 98.2, 89.3, 92.1, 97.8, 97.8, 91.5, 96.3, 87.2, 93.6, 95.1]
        }
        df_sample = pd.DataFrame(sample_data)
        df_sample.to_csv('sample_data.csv', index=False)
        st.success("Sample data created! Please upload the 'sample_data.csv' file above.")
