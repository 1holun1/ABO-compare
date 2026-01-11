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
# -----------------------------------------------------------------------------
# 3. THE UI AND COMPARISON LOGIC (ORDERED & UNCOLORED)
# -----------------------------------------------------------------------------
st.title("💊 Antibiotic Coverage Comparison")

if not df.empty:
    # 1. Identify classification (Type) and antibiotic columns
    classification_col = df.columns[0] 
    antibiotic_list = df.columns[1:].tolist()
    
    selected_antibiotics = st.multiselect(
        "Search and compare antibiotics:", 
        options=antibiotic_list, 
        placeholder="Select antibiotics..."
    )

    if selected_antibiotics:
        st.divider()
        
        # 2. Filter: rows where at least one selected antibiotic has data
        mask = df[selected_antibiotics].notna().any(axis=1)
        
        # 3. Order the columns: Classification first, then Antibiotics
        display_cols = [classification_col] + selected_antibiotics
        comparison_df = df.loc[mask, display_cols]
        
        # 4. UPDATED STYLING FUNCTION
        # We use 'subset' in the applymap to avoid coloring the first column
        def highlight_diff(val):
            if pd.isna(val) or val == "":
                return 'background-color: #f0f2f6; color: #999999' # Gray
            if str(val).upper() == 'V':
                return 'background-color: #ffeeba; color: black'   # Yellow
            return 'background-color: #d4edda; color: black'       # Green

        st.subheader("Comparison Results")
        
        # We apply styling ONLY to the antibiotic columns
        # This keeps the 'Type' column (the first one) clean and uncolored
        styled_df = comparison_df.style.applymap(
            highlight_diff, 
            subset=selected_antibiotics
        )
        
        st.dataframe(styled_df, use_container_width=True)

# 4. SIDEBAR
with st.sidebar:
    st.write("### Legend")
    st.info("**Green**: Susceptible (✔/S)\n\n**Yellow**: Variable (V)\n\n**Gray**: No Coverage/Resistant")
