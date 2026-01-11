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

# 3. THE UI AND COMPARISON LOGIC (REPLACED SECTION)
st.title("💊 Antibiotic Coverage Comparison")
st.markdown("Select multiple antibiotics to compare their bacterial coverage side-by-side.")

if not df.empty:
    # Changed from selectbox to multiselect
    antibiotic_list = df.columns.tolist()
    selected_antibiotics = st.multiselect(
        "Search and compare antibiotics:", 
        options=antibiotic_list, 
        placeholder="Select antibiotics (e.g., Penicillin G, Flucloxacillin...)"
    )

    if selected_antibiotics:
        st.divider()
        
        # FILTER LOGIC:
        # Create a 'mask' that finds rows where AT LEAST ONE selected column is not empty
        mask = df[selected_antibiotics].notna().any(axis=1)
        
        # Create the comparison table
        comparison_df = df.loc[mask, selected_antibiotics]
        
        # UPDATED STYLING FUNCTION:
        def highlight_diff(val):
            if pd.isna(val) or val == "":
                return 'background-color: #f0f2f6; color: #999999' # Gray for No Coverage
            if str(val).upper() == 'V':
                return 'background-color: #ffeeba; color: black'   # Yellow for Variable
            return 'background-color: #d4edda; color: black'       # Green for Susceptible

        st.subheader("Comparison Results")
        st.write("The table below shows all bacteria covered by *at least one* of your selections.")
        
        # Display the interactive table
        st.dataframe(
            comparison_df.style.applymap(highlight_diff), 
            use_container_width=True,
            height=400
        )
    else:
        st.info("💡 Start typing above to select and compare antibiotics.")

else:
    st.error("Please ensure 'ABO_data.xlsx' is in the folder.")

# 4. SIDEBAR
with st.sidebar:
    st.write("### Legend")
    st.info("**Green**: Susceptible (✔/S)\n\n**Yellow**: Variable (V)\n\n**Gray**: No Coverage/Resistant")
