import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Antibiotic Comparison Tool", page_icon="💊", layout="wide")

# 2. LOAD DATA
@st.cache_data
def load_data():
    try: 
        # Using your filename 'ABO_data.xlsx'
        df = pd.read_excel("ABO_data.xlsx", index_col=0)
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

# -----------------------------------------------------------------------------
# 3. THE UI AND COMPARISON LOGIC (WITH CLASSIFICATION)
# -----------------------------------------------------------------------------
st.title("💊 Antibiotic Coverage Comparison")
st.markdown("Compare antibiotic coverage with bacterial classification (Gram stain/Type).")

if not df.empty:
    # Identify antibiotic columns (everything except 'Type')
    # We use 'Type' because that is the name in your Excel image
    all_columns = df.columns.tolist()
    antibiotic_list = [col for col in all_columns if col != 'Type']
    
    selected_antibiotics = st.multiselect(
        "Search and compare antibiotics:", 
        options=antibiotic_list, 
        placeholder="Select antibiotics..."
    )

    if selected_antibiotics:
        st.divider()
        
        # FILTER LOGIC:
        # Rows where at least one selected antibiotic has data
        mask = df[selected_antibiotics].notna().any(axis=1)
        
        # Create display table: Always include 'Type' followed by selections
        display_columns = ['Type'] + selected_antibiotics
        comparison_df = df.loc[mask, display_columns]
        
        # STYLING FUNCTION
        def highlight_diff(val):
            # Do not color the classification text
            classification_keywords = ['Anaerobes', 'Atypical', 'Gram Positive', 'Gram Negative']
            if any(key in str(val) for key in classification_keywords):
                return ''
            
            if pd.isna(val) or val == "":
                return 'background-color: #f0f2f6; color: #999999' # Gray
            if str(val).upper() == 'V':
                return 'background-color: #ffeeba; color: black'   # Yellow
            return 'background-color: #d4edda; color: black'       # Green

        st.subheader("Comparison Results")
        st.dataframe(
            comparison_df.style.applymap(highlight_diff), 
            use_container_width=True
        )
else:
    st.error("Data could not be loaded. Check your file name in the code.")

# 4. SIDEBAR
with st.sidebar:
    st.write("### Legend")
    st.info("**Green**: Susceptible (✔/S)\n\n**Yellow**: Variable (V)\n\n**Gray**: No Coverage/Resistant")
