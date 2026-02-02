import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Set page configuration
st.set_page_config(page_title="Data Cleaning & Analysis Tool", layout="wide", page_icon="📊")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📊 Data Cleaning & Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("**Mini Project by:** [Your Name] | **Topic:** Pandas Data Cleaning and Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Data", "Data Overview", "Data Cleaning", "Analysis", "Visualization", "Export Data"])

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None

# ==================== PAGE 1: Upload Data ====================
if page == "Upload Data":
    st.markdown('<h2 class="section-header">📁 Upload Your Dataset</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.success(f"✅ File uploaded successfully! Shape: {df.shape}")
                st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")
    
    with col2:
        st.info("💡 **Tip:** Upload a CSV file to begin analysis")
        if st.button("📥 Load Sample Dataset"):
            # Create sample dataset with common data quality issues
            np.random.seed(42)
            sample_data = {
                'Student_ID': range(1, 51),
                'Name': [f'Student_{i}' for i in range(1, 51)],
                'Age': np.random.choice([18, 19, 20, 21, 22, None, -5, 150], 50),
                'Gender': np.random.choice(['Male', 'Female', 'male', 'MALE', None], 50),
                'Math_Score': np.random.randint(0, 101, 50),
                'Science_Score': np.random.randint(0, 101, 50),
                'English_Score': np.random.choice(list(range(0, 101)) + [None], 50),
                'Attendance_%': np.random.uniform(50, 100, 50),
                'Email': [f'student{i}@example.com' if i % 7 != 0 else None for i in range(1, 51)],
            }
            # Add some duplicates
            df = pd.DataFrame(sample_data)
            df = pd.concat([df, df.iloc[[5, 10, 15]]], ignore_index=True)
            
            st.session_state.df = df
            st.success("✅ Sample dataset loaded!")
            st.dataframe(df.head(10), use_container_width=True)

# ==================== PAGE 2: Data Overview ====================
elif page == "Data Overview":
    st.markdown('<h2 class="section-header">🔍 Data Overview</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        df = st.session_state.df
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        with col4:
            st.metric("Duplicate Rows", df.duplicated().sum())
        
        st.markdown("### 📋 Dataset Preview")
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### 📊 Data Types")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.values,
                'Non-Null Count': df.count().values
            }))
        
        with col2:
            st.markdown("### 📉 Missing Values Summary")
            missing_data = pd.DataFrame({
                'Column': df.columns,
                'Missing Count': df.isnull().sum().values,
                'Missing %': (df.isnull().sum().values / len(df) * 100).round(2)
            })
            missing_data = missing_data[missing_data['Missing Count'] > 0]
            if len(missing_data) > 0:
                st.dataframe(missing_data, use_container_width=True)
            else:
                st.success("✅ No missing values found!")
        
        st.markdown("### 📈 Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)

# ==================== PAGE 3: Data Cleaning ====================
elif page == "Data Cleaning":
    st.markdown('<h2 class="section-header">🧹 Data Cleaning Operations</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        df = st.session_state.df.copy()
        
        st.markdown("### Select Cleaning Operations:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            remove_duplicates = st.checkbox("Remove Duplicate Rows", value=True)
            handle_missing = st.checkbox("Handle Missing Values", value=True)
            if handle_missing:
                missing_strategy = st.selectbox("Missing Value Strategy", 
                    ["Drop rows with missing values", "Fill with mean (numeric)", "Fill with median (numeric)", "Fill with mode"])
        
        with col2:
            standardize_text = st.checkbox("Standardize Text (lowercase)", value=True)
            remove_outliers = st.checkbox("Remove Outliers (numeric columns)", value=False)
            if remove_outliers:
                outlier_threshold = st.slider("Z-score threshold", 1.0, 4.0, 3.0)
        
        if st.button("🚀 Apply Cleaning Operations"):
            with st.spinner("Cleaning data..."):
                original_shape = df.shape
                
                # Remove duplicates
                if remove_duplicates:
                    df = df.drop_duplicates()
                    st.info(f"Removed {original_shape[0] - df.shape[0]} duplicate rows")
                
                # Handle missing values
                if handle_missing:
                    if missing_strategy == "Drop rows with missing values":
                        df = df.dropna()
                    elif missing_strategy == "Fill with mean (numeric)":
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        for col in numeric_cols:
                            df[col].fillna(df[col].mean(), inplace=True)
                    elif missing_strategy == "Fill with median (numeric)":
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        for col in numeric_cols:
                            df[col].fillna(df[col].median(), inplace=True)
                    elif missing_strategy == "Fill with mode":
                        for col in df.columns:
                            if df[col].isnull().sum() > 0:
                                df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
                    st.info(f"Handled missing values using: {missing_strategy}")
                
                # Standardize text
                if standardize_text:
                    text_cols = df.select_dtypes(include=['object']).columns
                    for col in text_cols:
                        df[col] = df[col].astype(str).str.strip().str.lower()
                    st.info(f"Standardized text in {len(text_cols)} columns")
                
                # Remove outliers
                if remove_outliers:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    for col in numeric_cols:
                        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                        df = df[z_scores < outlier_threshold]
                    st.info(f"Removed outliers using z-score threshold: {outlier_threshold}")
                
                st.session_state.cleaned_df = df
                st.success(f"✅ Cleaning complete! New shape: {df.shape} (Original: {original_shape})")
                
                st.markdown("### 🎯 Cleaned Data Preview")
                st.dataframe(df.head(20), use_container_width=True)

# ==================== PAGE 4: Analysis ====================
elif page == "Analysis":
    st.markdown('<h2 class="section-header">📊 Data Analysis</h2>', unsafe_allow_html=True)
    
    df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    
    if df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        st.markdown("### 🔢 Numerical Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Summary Statistics")
                selected_col = st.selectbox("Select column for detailed analysis", numeric_cols)
                
                if selected_col:
                    col_data = df[selected_col].dropna()
                    
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    with metrics_col1:
                        st.metric("Mean", f"{col_data.mean():.2f}")
                        st.metric("Min", f"{col_data.min():.2f}")
                    with metrics_col2:
                        st.metric("Median", f"{col_data.median():.2f}")
                        st.metric("Max", f"{col_data.max():.2f}")
                    with metrics_col3:
                        st.metric("Std Dev", f"{col_data.std():.2f}")
                        st.metric("Count", len(col_data))
            
            with col2:
                st.markdown("#### Correlation Matrix")
                if len(numeric_cols) > 1:
                    corr_matrix = df[numeric_cols].corr()
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax, fmt='.2f')
                    ax.set_title('Correlation Matrix')
                    st.pyplot(fig)
                    plt.close()
        
        st.markdown("### 📋 Categorical Analysis")
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(cat_cols) > 0:
            selected_cat = st.selectbox("Select categorical column", cat_cols)
            if selected_cat:
                value_counts = df[selected_cat].value_counts()
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"#### Value Counts: {selected_cat}")
                    st.dataframe(pd.DataFrame({
                        'Value': value_counts.index,
                        'Count': value_counts.values,
                        'Percentage': (value_counts.values / len(df) * 100).round(2)
                    }))
                
                with col2:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    value_counts.plot(kind='bar', ax=ax, color='skyblue')
                    ax.set_title(f'Distribution of {selected_cat}')
                    ax.set_xlabel(selected_cat)
                    ax.set_ylabel('Count')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()

# ==================== PAGE 5: Visualization ====================
elif page == "Visualization":
    st.markdown('<h2 class="section-header">📈 Data Visualization</h2>', unsafe_allow_html=True)
    
    df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    
    if df is None:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        viz_type = st.selectbox("Select Visualization Type", 
            ["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Pie Chart", "Bar Chart"])
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if viz_type == "Histogram":
            if len(numeric_cols) > 0:
                col = st.selectbox("Select column", numeric_cols)
                bins = st.slider("Number of bins", 5, 50, 20)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.hist(df[col].dropna(), bins=bins, color='steelblue', edgecolor='black')
                ax.set_title(f'Histogram of {col}')
                ax.set_xlabel(col)
                ax.set_ylabel('Frequency')
                ax.grid(axis='y', alpha=0.3)
                st.pyplot(fig)
                plt.close()
        
        elif viz_type == "Box Plot":
            if len(numeric_cols) > 0:
                cols = st.multiselect("Select columns", numeric_cols, default=numeric_cols[:3])
                if cols:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    df[cols].boxplot(ax=ax)
                    ax.set_title('Box Plot')
                    ax.set_ylabel('Values')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
        
        elif viz_type == "Scatter Plot":
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols)
                with col2:
                    y_col = st.selectbox("Y-axis", [c for c in numeric_cols if c != x_col])
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.scatter(df[x_col], df[y_col], alpha=0.6, color='coral')
                ax.set_title(f'{y_col} vs {x_col}')
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.grid(alpha=0.3)
                st.pyplot(fig)
                plt.close()
        
        elif viz_type == "Line Chart":
            if len(numeric_cols) > 0:
                cols = st.multiselect("Select columns", numeric_cols, default=numeric_cols[:2])
                if cols:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    for col in cols:
                        ax.plot(df.index, df[col], marker='o', label=col, linewidth=2)
                    ax.set_title('Line Chart')
                    ax.set_xlabel('Index')
                    ax.set_ylabel('Values')
                    ax.legend()
                    ax.grid(alpha=0.3)
                    st.pyplot(fig)
                    plt.close()
        
        elif viz_type == "Pie Chart":
            if len(cat_cols) > 0:
                col = st.selectbox("Select categorical column", cat_cols)
                top_n = st.slider("Show top N categories", 3, 15, 5)
                
                value_counts = df[col].value_counts().head(top_n)
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
                ax.set_title(f'Distribution of {col} (Top {top_n})')
                st.pyplot(fig)
                plt.close()
        
        elif viz_type == "Bar Chart":
            if len(cat_cols) > 0 and len(numeric_cols) > 0:
                cat_col = st.selectbox("Categorical column (X-axis)", cat_cols)
                num_col = st.selectbox("Numerical column (Y-axis)", numeric_cols)
                
                grouped_data = df.groupby(cat_col)[num_col].mean().sort_values(ascending=False).head(10)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                grouped_data.plot(kind='bar', ax=ax, color='teal')
                ax.set_title(f'Average {num_col} by {cat_col}')
                ax.set_xlabel(cat_col)
                ax.set_ylabel(f'Average {num_col}')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

# ==================== PAGE 6: Export Data ====================
elif page == "Export Data":
    st.markdown('<h2 class="section-header">💾 Export Cleaned Data</h2>', unsafe_allow_html=True)
    
    df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.df
    
    if df is None:
        st.warning("⚠️ Please upload and clean a dataset first!")
    else:
        st.success(f"✅ Dataset ready for export! Shape: {df.shape}")
        
        st.markdown("### 📋 Final Dataset Preview")
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
        
        with col2:
            st.markdown("### 📊 Export Summary")
            st.info(f"""
            - **Total Rows:** {df.shape[0]}
            - **Total Columns:** {df.shape[1]}
            - **Missing Values:** {df.isnull().sum().sum()}
            - **File Size:** ~{len(csv) / 1024:.2f} KB
            """)

# Footer
st.markdown("---")
st.markdown("**🎓 Mini Project:** Pandas Data Cleaning and Analysis | **Made with Streamlit**")
