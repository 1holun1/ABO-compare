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
# -----------------------------------------------------------------------------
# 3. THE UI AND COMPARISON LOGIC (FINAL POLISHED VERSION)
# -----------------------------------------------------------------------------
st.title("💊 Antibiotic Coverage Comparison")

if not df.empty:
    # Identify the classification column and antibiotic names
    classification_col = df.columns[0] 
    antibiotic_list = df.columns[1:].tolist()
    
    selected_antibiotics = st.multiselect(
        "Search and compare antibiotics:", 
        options=antibiotic_list, 
        placeholder="Select antibiotics..."
    )

    if selected_antibiotics:
        st.divider()
        
        # 1. Filter: Find rows where any selected antibiotic has a value
        mask = df[selected_antibiotics].notna().any(axis=1)
        
        # 2. Arrange Columns: [Classification/Type] + [Selected Antibiotics]
        display_cols = [classification_col] + selected_antibiotics
        comparison_df = df.loc[mask, display_cols].copy()
        
        # 3. STYLING FUNCTION
        def highlight_diff(val):
            # Convert to string and clean up for checking
            v_str = str(val).strip().lower()
            
            # Handle empty/None cells (Gray)
            if pd.isna(val) or v_str == "" or v_str == 'none':
                return 'background-color: #f0f2f6; color: #999999'
            
            # Handle Variable coverage (Yellow)
            if v_str == 'v':
                return 'background-color: #ffeeba; color: black'
            
            # Handle Susceptible (Green)
            return 'background-color: #d4edda; color: black'

        st.subheader("Comparison Results")
        
        # 4. TARGETED STYLING: 
        # We tell the map function to ONLY look at the antibiotic columns.
        # This keeps your 'Type' column clean and professional.
        styled_df = comparison_df.style.map(
            highlight_diff, 
            subset=selected_antibiotics
        )
        
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("💡 Select antibiotics above to begin comparison.")

# 4. SIDEBAR
with st.sidebar:
    st.write("### Legend")
    st.info("**Green**: Susceptible (✔/S)\n\n**Yellow**: Variable (V)\n\n**Gray**: No Coverage/Resistant")
