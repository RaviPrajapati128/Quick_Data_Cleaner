import streamlit as st
import pandas as pd 
from sklearn.impute import SimpleImputer

st.title("Quick Data Cleaner🧹")

st.subheader("Clean and preprocess your CSV datasets with ease!")

data = st.file_uploader(" ",type=["csv"])

if data is not None:
    try:
        if data.size == 0:
            st.error("The uploaded file is empty. Please upload a valid CSV.")
        else:     
            file = pd.read_csv(data)
            st.subheader("Data Preview:")
            st.write(file)
            df = pd.DataFrame(file)
            
            def clear(cos):
                if cos is not None:
                    st.subheader("Remove Columns")
                    file.drop(columns = cos,inplace=True)
                    st.success(f"{cos} removed")
                    st.write(file)
            st.markdown("---")
            #df = pd.DataFrame(file)
            #st.write(list(df.columns))
            def avg(cos):
                if cos is not None:
                    si = SimpleImputer(strategy = "mean")
                    ar = si.fit_transform(file[list(cos)])
                    new_data = pd.DataFrame(ar,columns=cos)
                    st.success("Columns Are Filled With Mean:")
                    st.write(new_data)
        
            def mod_e(cos):
                if cos is not None:
                    si = SimpleImputer(strategy = "most_frequent")
                    ar = si.fit_transform(file[list(cos)])
                    new_data = pd.DataFrame(ar,columns=cos)
                    st.success("Columns Are Filled With Mode:")
                    st.write(new_data)
        
            def media_n(cos):
                if cos is not None:
                    si = SimpleImputer(strategy = "median")
                    ar = si.fit_transform(file[list(cos)])
                    new_data = pd.DataFrame(ar,columns=cos)
                    st.success("Columns Are Filled With Median:")
                    st.write(new_data)
                        
        
            st.sidebar.subheader("Look Into Data")
                
            z = st.sidebar.selectbox(" ",["Describe Data","Show Null Values","Data Quality","Information","Column Name","Shape"])
            if z == "Show Null Values":
                blanks =file.isnull().sum()
                st.subheader("ColumnWise Blank Values")
                st.write(blanks)
                st.write("Total Blank Values:",blanks.sum())
                    
            if z == "Column Name":
                st.write("Column Name:",list(df.columns))
            
            if z == "Shape" :
                st.subheader("Shape")
                r = str(file.shape[0])
                c = str(file.shape[1])
                st.write("Rows:",r)
                st.write("Columns:",c)
            
            if z == "Describe Data" :
                st.subheader("About Data")
                st.text(file.describe())
            
            if z == "Information" :
                st.subheader("Information")
                st.text(file.info())
                    
            if z == "Data Quality":
                st.subheader("Data Quality% Column Wise")
                y = pd.DataFrame((file.isnull().sum()/file.shape[0])*100)
                y
                if st.button("Bar_Graph"):
                    st.bar_chart(y)
                    st.write("Total Null%:",(file.isnull().sum().sum()/(file.shape[0]*file.shape[1]))*100)
                
            st.markdown("---")
                    
            st.sidebar.subheader("Remove Columns")
        
            if st.sidebar.button("Remove All Null Values"):
               st.success("Null Values Are Removed")
               file.dropna(inplace=True)
               st.write(file)
               st.write("Null Values in Columns",file.isnull().sum())
        
            cos = st.sidebar.multiselect("Remove Columns ",list(df.columns))
            if cos is not None:
                clear(cos)
        
            st.sidebar.subheader("Fill Columns")
        
            Method = st.sidebar.selectbox("Methods To Fill Null Values:",[" ","Bfill","Ffill"])
            if Method == "Bfill":
                st.success("Bfill Done")
                st.write(file.ffill())
            elif Method == "Ffill":
                st.success("Ffill Done")
                st.write(file.ffill())
                
            datatype = st.sidebar.selectbox("Smart Fill:",[" ","float64","Object"])
            
            if datatype == "float64":
                p = file.select_dtypes(include="float64").columns
                lst = st.write("columns:",list(p))
                si = SimpleImputer(strategy = "mean")
                ar = si.fit_transform(file[list(p)])
                new_data = pd.DataFrame(ar,columns=file.select_dtypes(include="float64").columns)
                st.success("Numerical Columns Are Filled With Mean")
                st.write(new_data)
            
            if datatype == "Object":
                p = file.select_dtypes(include="object").columns
                lst = st.write("columns:",list(p))
                si = SimpleImputer(strategy = "most_frequent")
                ar = si.fit_transform(file[list(p)])
                new_data = pd.DataFrame(ar,columns=file.select_dtypes(include="object").columns)
                st.success("Categorical Columns Are Filled with Mode")
                st.write(new_data)
                st.markdown("---")
            
            cos = st.sidebar.multiselect("Fill Mean", list(df.columns))
            if cos:  
                numeric_cols = df[cos].select_dtypes(include=['number']).columns
                object_cols = df[cos].select_dtypes(include=['object']).columns
        
                if len(numeric_cols) > 0:
                    avg(numeric_cols)   # only pass numeric columns
                    st.success(f"Applied Fill Mean on: {list(numeric_cols)}")
                if len(object_cols) > 0:
                    st.warning(f"Skipped object columns: {list(object_cols)}")
        
        
            cos = st.sidebar.multiselect("Fill Mode", list(df.columns))
            if not cos : 
                st.write(" ")
            else:
                mod_e(cos)
        
            cos = st.sidebar.multiselect("Fill Median", list(df.columns))
            if cos: 
                numeric_cols = df[cos].select_dtypes(include=['number']).columns
                object_cols = df[cos].select_dtypes(include=['object']).columns
        
                if len(numeric_cols) > 0:
                    media_n(numeric_cols)   # only pass numeric columns
                    st.success(f"Applied Fill Median on: {list(numeric_cols)}")
                if len(object_cols) > 0:
                    st.warning(f"Skipped object columns: {list(object_cols)}")
            
    except pd.errors.EmptyDataError:
        st.error("The uploaded file has no data or is not a valid CSV.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.warning("Please upload a file.")

st.markdown("### 📌 User Description")
st.markdown("""
- 🧹 **Quick Data Cleaner** is a Streamlit app that helps users clean and preprocess CSV datasets.  
- 📊 Upload data, preview it instantly, and explore structure, null values, and quality metrics.  
- 🗑️ Remove unwanted columns or rows with missing values in just one click.  
- 🔄 Fill missing data using mean, median, mode, forward fill, or backward fill strategies.  
- ✅ Get instant feedback with success and warning messages, making data cleaning simple and interactive.  
""")





