
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
# 3. TABS AND SEARCH LOGIC
# -----------------------------------------------------------------------------

# Create the tabs
tab1, tab2 = st.tabs(["💊 Compare Antibiotics", "🦠 Search Bacteria"])

if not df.empty:
    bacteria_col = df.columns[0]
    type_col = df.columns[1]
    antibiotic_list = df.columns[2:].tolist()

    # --- TAB 1: YOUR EXISTING LOGIC ---
    with tab1:
        st.subheader("Compare Coverage")
        selected_antibiotics = st.multiselect(
            "Select antibiotics to see their spectrum:", 
            options=antibiotic_list,
            placeholder="Choose antibiotics...",
            key="tab1_multi"
        )
        
        if selected_antibiotics:
            mask = df[selected_antibiotics].notna().any(axis=1)
            display_cols = [type_col, bacteria_col] + selected_antibiotics
            comparison_df = df.loc[mask, display_cols].copy()
            
            # Styling
            def highlight_tab1(val):
                v_str = str(val).strip().lower()
                if pd.isna(val) or v_str == "" or v_str == 'none':
                    return 'background-color: #f0f2f6; color: #999999'
                if v_str == 'v':
                    return 'background-color: #ffeeba; color: black'
                return 'background-color: #d4edda; color: black'

            st.dataframe(
                comparison_df.style.map(highlight_tab1, subset=selected_antibiotics),
                use_container_width=True,
                hide_index=True,
                column_config={type_col: st.column_config.TextColumn("Type", width="small")}
            )
        else:
            # Buffer space to force dropdown DOWN
            for _ in range(10): st.write("")

    # --- TAB 2: THE NEW SEARCH FUNCTION ---
    with tab2:
        st.subheader("What covers this bacterium?")
        selected_organism = st.selectbox(
            "Search for a bacterium:",
            options=df[bacteria_col].unique(),
            index=None,
            placeholder="Type bacteria name here...",
            key="tab2_select"
        )

        if selected_organism:
            # Get the row for this bacterium
            row = df[df[bacteria_col] == selected_organism].iloc[0]
            
            st.markdown(f"**Classification:** {row[type_col]}")
            
            # Filter columns that have data (exclude the Bacteria and Type columns)
            # We filter for values that are NOT NA and NOT "None"
            coverage = row[antibiotic_list].dropna()
            coverage = coverage[coverage.astype(str).str.lower() != 'none']
            
            if not coverage.empty:
                # Create a simple DataFrame for display
                res_df = pd.DataFrame({
                    "Antibiotic": coverage.index,
                    "Effectiveness": coverage.values
                })

                # Styling for the lookup
                def highlight_tab2(val):
                    if str(val).upper() == 'V':
                        return 'background-color: #ffeeba; color: black'
                    return 'background-color: #d4edda; color: black'

                st.table(res_df.style.map(highlight_tab2, subset=['Effectiveness']))
            else:
                st.warning("No antibiotic data found for this organism in the current database.")
        else:
            # Buffer space to force dropdown DOWN
            for _ in range(10): st.write("")

  

# 4. SIDEBAR
with st.sidebar:
    st.write("### Legend")
    st.info("**Green (✔)**: Susceptible\n\n**Yellow (V)**: Variable \n\n**Gray**: No data/ Resistant")
