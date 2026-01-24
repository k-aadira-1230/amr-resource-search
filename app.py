import streamlit as st
import pandas as pd

st.title("AMR Resource Search")
st.write("Search antimicrobial resistance databases and computational tools")
st.sidebar.header("Filters")

# apply clear filter

if st.sidebar.button("Clear all filters"):
    st.session_state.category = []
    st.session_state.data_type = []
    st.session_state.target_user = []
    st.session_state.methodology = []
    st.session_state.access_type = []
    st.session_state.interface = []
    st.rerun()

#load dataset
@st.cache_data
def load_data():
    return pd.read_excel("AMR_Databases_and_Tools.xlsx", sheet_name="AMR_Databases_and_Tools")

@st.cache_data
def load_controlled_vocab():
    return pd.read_excel(
        "AMR_Databases_and_Tools.xlsx",
        sheet_name="Controlled_Vocabulary"
    )
df = load_data()

# load controlled vocabulary

cv = load_controlled_vocab()

def get_vocab(column_name):
    return (
        cv[column_name]
        .dropna()
        .astype(str)
        .str.lower()
        .str.strip()
        .unique()
        .tolist()
    )

multi_value_cols = [
    "data_type",
    "methodology",
    "interface",
    "category",
    "target_user",
    "access_type"
]

for col in multi_value_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.lower()
        .str.strip()
    )

def normalize_cell(cell):
    return [
        v.strip().lower()
        for v in str(cell)
        .replace("|", ",")
        .replace(";", ",")
        .replace("/", ",")
        .split(",")
    ]

def filter_multi_value(df, column, selected_values):
    selected_values = [v.lower().strip() for v in selected_values]

    return df[
        df[column].apply(
            lambda cell: any(
                val in normalize_cell(cell)
                for val in selected_values
            )
        )
    ]

# Get unique values for filters
categories = get_vocab("category")
data_types = get_vocab("data_type")
target_users = get_vocab("target_user")
methodologies = get_vocab("methodology")
access_types = get_vocab("access_type")
interfaces = get_vocab("interface")

# Sidebar filters
selected_category = st.sidebar.multiselect(
    "Category", categories, key="category"
)
selected_data_type = st.sidebar.multiselect(
    "Data type", data_types, key="data_type"
)
selected_target_user = st.sidebar.multiselect(
    "Target user", target_users, key="target_user"
)
selected_methodology = st.sidebar.multiselect(
    "Methodology", methodologies, key="methodology"
)
selected_access_type = st.sidebar.multiselect(
    "Access type", access_types, key="access_type"
)
selected_interface = st.sidebar.multiselect(
    "Interface", interfaces, key="interface"
)

search_query = st.text_input("Search AMR resources")

# apply filters

result_df = df.copy()

if selected_data_type:
    result_df = filter_multi_value(result_df, "data_type", selected_data_type)

if selected_methodology:
    result_df = filter_multi_value(result_df, "methodology", selected_methodology)

if selected_interface:
    result_df = filter_multi_value(result_df, "interface", selected_interface)

if selected_category:
    result_df = filter_multi_value(result_df, "category", selected_category)

if selected_target_user:
    result_df = filter_multi_value(result_df, "target_user", selected_target_user)

if selected_access_type:
    result_df = filter_multi_value(result_df, "access_type", selected_access_type)


# apply search (ranking strategy)

if search_query:
    query = search_query.lower().strip()

    weights = {
        "database/tool_name": 4,
        "tags": 3,
        "primary_use": 2,
        "description": 1
    }

    def compute_score(row):
        score = 0
        for col, weight in weights.items():
            value = str(row[col]).lower()
            if query in value:
                score += weight
        return score

    result_df["score"] = result_df.apply(compute_score, axis=1)
    result_df = result_df[result_df["score"] > 0]
    result_df = result_df.sort_values("score", ascending=False)
    result_df = result_df.drop(columns=["score"])

# display logic

has_filters = any([
    selected_category,
    selected_data_type,
    selected_access_type,
    selected_target_user,
    selected_methodology,
    selected_interface
])

has_search = bool(search_query)

if has_filters and not has_search:
    result_df = result_df.sort_values("database/tool_name")

if not has_filters and not has_search:
    st.info("Use the search bar or filters on the left to discover AMR resources.")
else:
    st.caption(f"Showing {len(result_df)} matching AMR resources")

    for _, row in result_df.iterrows():
        # Resource name
        st.markdown(f"### {row['database/tool_name']}")

        # Clickable link
        if pd.notna(row["url"]):
            st.markdown(f"[{row['url']}]({row['url']})")

        # Primary use
        if pd.notna(row["primary_use"]):
            st.markdown(f"**Primary use:** {row['primary_use']}")

        # Description
        if pd.notna(row["description"]):
            st.markdown(row["description"])

        st.divider()