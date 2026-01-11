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
# 3. THE UI AND COMPARISON LOGIC (TYPE ON THE FAR LEFT)
# -----------------------------------------------------------------------------
st.title("💊 Antibiotic Coverage Comparison")

if not df.empty:
    # 1. Identify your columns by their position
    # df.columns[0] is Bacteria Name
    # df.columns[1] is Type/Classification
    bacteria_col = df.columns[0]
    type_col = df.columns[1]
    antibiotic_list = df.columns[2:].tolist()
    
    selected_antibiotics = st.multiselect(
        "Search and compare antibiotics:", 
        options=antibiotic_list, 
        placeholder="Select antibiotics..."
    )

    if selected_antibiotics:
        st.divider()
        
        # 2. Filter: rows where at least one selected antibiotic has data
        mask = df[selected_antibiotics].notna().any(axis=1)
        
        # 3. NEW ORDER: [Type, Bacteria Name, Antibiotics]
        display_cols = [type_col, bacteria_col] + selected_antibiotics
        comparison_df = df.loc[mask, display_cols]
        
        # 4. STYLING
        def highlight_diff(val):
            v_str = str(val).strip().lower()
            if pd.isna(val) or v_str == "" or v_str == 'none':
                return 'background-color: #f0f2f6; color: #999999'
            if v_str == 'v':
                return 'background-color: #ffeeba; color: black'
            return 'background-color: #d4edda; color: black'

        st.subheader("Comparison Results")
        
        # Apply style ONLY to antibiotic columns to keep Type/Name clean
        styled_df = comparison_df.style.map(
            highlight_diff, 
            subset=selected_antibiotics
        )
        
        # Hide the default index (the 0, 1, 2, 3 numbers)
# --- Display with custom column widths ---
# 6. DISPLAY WITH COLUMN WIDTH CONFIGURATION
        st.dataframe(
            styled_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                type_col: st.column_config.TextColumn(
                    "Type",
                    width="small",  # Only keep the Type column narrow
                )
                # Bacteria column is removed from here so it auto-sizes
            }
        )

  

# 4. SIDEBAR
with st.sidebar:
    st.write("### Legend")
    st.info("**Green (✔)**: Susceptible\n\n**Yellow (V)**: Variable \n\n**Gray**: No data/ Resistant")
