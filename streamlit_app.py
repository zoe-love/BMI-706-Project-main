import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

# Move this code into `load_data` function {{
# }}

@st.cache
def load_data():
    ## {{ CODE HERE }} ##
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
)

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Sex"],
    var_name="Age",
    value_name="Pop",
)

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    return df

df = load_data()

### P1.2 ###


st.write("## Age-specific cancer mortality rates - TEST TEST TEST")

### P2.1 ###
# replace with st.slider

year = st.slider(label = "Year Select", min_value = 1994, max_value = 2020, value = 2012)
subset = df[df["Year"] == year]
### P2.1 ###


### P2.2 ###
# replace with st.radio
sex = st.radio(label = "Gender Select", options = ('F', 'M'))
subset = subset[subset["Sex"] == sex]
### P2.2 ###


### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = st.multiselect(label = 'Country Select', 
    options = ["Austria",
        "Germany",
        "Iceland",
        "Spain",
        "Sweden",
        "Thailand",
        "Turkey"], 
    default = [
        "Austria",
        "Germany",
        "Iceland",
        "Spain",
        "Sweden",
        "Thailand",
        "Turkey",
]
)
subset = subset[subset["Country"].isin(countries)]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox
cancer = st.selectbox(label ="Cancer", 
        options = ['Leukaemia', 'Malignant melanoma of skin',
       'Malignant neoplasm of bladder', 'Malignant neoplasm of breast',
       'Malignant neoplasm of cervix uteri',
       'Malignant neoplasm of colon  rectum and anus',
       'Malignant neoplasm of larynx',
       'Malignant neoplasm of lip oral cavity and pharynx',
       'Malignant neoplasm of liver and intrahepatic bile ducts',
       'Malignant neoplasm of meninges  brain and other parts of central nervous system',
       'Malignant neoplasm of oesophagus',
       'Malignant neoplasm of other and unspecified parts of uterus',
       'Malignant neoplasm of ovary', 'Malignant neoplasm of pancreas',
       'Malignant neoplasm of prostate', 'Malignant neoplasm of stomach',
       'Malignant neoplasm of trachea  bronchus and lung',
       'Multiple myeloma and malignant plasma cell neoplasms',
       "Non-Hodgkin's lymphoma", 'Remainder of malignant neoplasms'], index = 0)
subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Country:N"),
    color=alt.Color("Rate", scale = alt.Scale(clamp=True, domain=[0.01, 1000], type="log")),
    tooltip=["Rate:Q"],
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
