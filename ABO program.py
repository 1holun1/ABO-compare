import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Antibiotic Comparison Tool", page_icon="💊", layout="wide")

# 2. LOAD DATA
@st.cache_data
def load_data():
    try: 
        # Using your filename 'ABO_data.xlsx'
        df = pd.read_excel("ABO_data.xlsx", index_col=None)
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 3. THE UI AND COMPARISON LOGIC (SIDEBAR VERSION)
# -----------------------------------------------------------------------------
st.title("💊 Antibiotic Coverage Comparison")

if not df.empty:
    # 1. Setup column names
    bacteria_col = df.columns[0]
    type_col = df.columns[1]
    antibiotic_list = df.columns[2:].tolist()
    
    # 2. MOVE THE SELECTION TO THE SIDEBAR
    with st.sidebar:
        st.header("Settings")
        selected_antibiotics = st.multiselect(
            "Select antibiotics to compare:", 
            options=antibiotic_list, 
            placeholder="Choose antibiotics..."
        )
        st.info("The dropdown menu here will usually expand downward as long as there is space in the sidebar.")

    # 3. MAIN AREA RESULTS
    if selected_antibiotics:
        # Filter logic
        mask = df[selected_antibiotics].notna().any(axis=1)
        display_cols = [type_col, bacteria_col] + selected_antibiotics
        comparison_df = df.loc[mask, display_cols].copy()
        
        # Styling
        def highlight_diff(val):
            v_str = str(val).strip().lower()
            if pd.isna(val) or v_str == "" or v_str == 'none':
                return 'background-color: #f0f2f6; color: #999999'
            if v_str == 'v':
                return 'background-color: #ffeeba; color: black'
            return 'background-color: #d4edda; color: black'

        styled_df = comparison_df.style.map(
            highlight_diff, 
            subset=selected_antibiotics
        )
        
        st.subheader("Comparison Results")
        st.dataframe(
            styled_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                type_col: st.column_config.TextColumn("Type", width="small")
            }
        )
    else:
        st.info("👈 Use the sidebar on the left to select antibiotics for comparison.")
  

# 4. SIDEBAR
with st.sidebar:
    st.write("### Legend")
    st.info("**Green (✔)**: Susceptible\n\n**Yellow (V)**: Variable \n\n**Gray**: No data/ Resistant")
