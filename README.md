# 📊 Data Cleaning & Analysis Dashboard

## Mini Project: Pandas Data Cleaning and Analysis

A comprehensive web-based data analytics tool built with Python, Pandas, NumPy, Matplotlib, and Streamlit.

### ✨ Features

- **Data Upload**: Upload CSV files or use sample dataset
- **Data Overview**: View dataset statistics, data types, and missing values
- **Data Cleaning**: 
  - Remove duplicate rows
  - Handle missing values (drop, fill with mean/median/mode)
  - Standardize text formatting
  - Remove outliers using z-score
- **Data Analysis**:
  - Numerical statistics (mean, median, std, min, max)
  - Correlation matrix with heatmap
  - Categorical value counts and distributions
- **Visualizations**:
  - Histogram
  - Box Plot
  - Scatter Plot
  - Line Chart
  - Pie Chart
  - Bar Chart
- **Data Export**: Download cleaned data as CSV

### 🚀 Deployment on Streamlit Cloud (100% FREE)

#### Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New Repository"
3. Name it: `data-analytics-mini-project`
4. Make it Public
5. Click "Create Repository"

#### Step 2: Upload Files to GitHub
1. Click "uploading an existing file"
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. Commit changes

#### Step 3: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `data-analytics-mini-project`
5. Main file path: `app.py`
6. Click "Deploy"
7. Wait 2-3 minutes for deployment
8. Your app will be live at: `https://[your-username]-data-analytics-mini-project.streamlit.app`

### 💻 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### 📊 Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical visualizations
- **Streamlit**: Web framework

### 📝 Project Components

1. **Data Loading**: CSV file upload with validation
2. **Data Profiling**: Automated quality checks
3. **Data Cleaning**: Multiple cleaning strategies
4. **Statistical Analysis**: Descriptive statistics and correlations
5. **Visualizations**: 6 different chart types
6. **Data Export**: Clean data download

### 🎯 Learning Outcomes

- CSV data handling with Pandas
- Data cleaning techniques
- Missing value treatment
- Outlier detection and removal
- Statistical analysis using NumPy
- Data visualization with Matplotlib
- Web app development with Streamlit

### 👤 Student Information

**Name**: [Your Name]  
**Project**: Mini Project #9 - Pandas Data Cleaning and Analysis  
**Course**: Data Analytics

### 📸 Screenshots

The application includes:
- Clean, professional UI
- Interactive data tables
- Multiple visualization types
- Real-time data processing
- Export functionality

### 🔧 Customization

To modify the sample dataset:
1. Open `app.py`
2. Find the "Load Sample Dataset" section
3. Modify the `sample_data` dictionary

### 📄 License

Free to use for educational purposes.

### 🆘 Troubleshooting

**Issue**: App crashes on deployment  
**Solution**: Check requirements.txt versions match your local environment

**Issue**: CSV upload fails  
**Solution**: Ensure CSV is properly formatted with headers

**Issue**: Visualizations not showing  
**Solution**: Check if numeric columns exist in dataset

### 📞 Support

For questions during viva:
- Explain the data flow: Upload → Clean → Analyze → Visualize → Export
- Discuss cleaning strategies: duplicates, missing values, outliers
- Show understanding of Pandas operations and NumPy calculations
- Demonstrate visualization interpretation

---

**Made with ❤️ using Python, Pandas, and Streamlit**
