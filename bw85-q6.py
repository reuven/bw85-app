import streamlit as st
import pandas as pd

filename = 'webk24.txt'

df = pd.read_csv(filename, sep='|',
                 header=None,
                 names= ['CMTE_ID',
                         'CMTE_NM', 'CMTE_TP', 'CMTE_DSGN',
                         'CMTE_FILING_FREQ', 'TTL_RECEIPTS', 'TRANS_FROM_AFF',
                         'INDV_CONTRIB', 'OTHER_POL_CMTE_CONTRIB',
                         'CAND_CONTRIB', 'CAND_LOANS', 'TTL_LOANS_RECEIVED',
                         'TTL_DISB', 'TRANF_TO_AFF', 'INDV_REFUNDS',
                         'OTHER_POL_CMTE_REFUNDS', 'CAND_LOAN_REPAY',
                         'LOAN_REPAY', 'COH_BOP', 'COH_COP', 'DEBTS_OWED_BY',
                         'NONFED_TRANS_RECEIVED', 'CONTRIB_TO_OTHER_CMTE',
                         'IND_EXP', 'PTY_COORD_EXP', 'NONFED_SHARE_EXP',
                         'CVG_END_DT'],
                 index_col='CMTE_ID')

# Committee name contains
committee_name_contains = st.text_input(
    'Committee name contains')

# Min/max raised
max_raised_value = int(df['TTL_RECEIPTS'].max() / 1000) + 1
min_raised = st.slider('Min raised (in thousands)',
                       min_value=0,
                       max_value=max_raised_value)
max_raised = st.slider('Max raised (in thousands)',
                       min_value=0,
                       max_value=max_raised_value,
                       value=max_raised_value)

if min_raised > max_raised:
    min_raised, max_raised = max_raised, min_raised

# Choose columns
columns_to_show = st.multiselect(
    'What columns to display?',
    df.columns,
    ['CMTE_NM', 'TTL_RECEIPTS'])

# Choose committee designations
designations_to_show = st.multiselect(
    'What designations to display?',
    df['CMTE_DSGN'].drop_duplicates(), ['B'])

filtered_df = (
    df
    .loc[lambda df_: df_['CMTE_DSGN'].isin(designations_to_show)]
    .loc[lambda df_: df_['TTL_RECEIPTS'] >= min_raised * 1000]
    .loc[lambda df_: df_['TTL_RECEIPTS'] <= max_raised * 1000]
    .loc[lambda df_:
         df_['CMTE_NM'].str.contains(committee_name_contains.upper())]
    [columns_to_show]
    )

st.title('PAC fund-raising explorer')
st.markdown('''Choose which columns you want to see, min/max donations, and/or part of the committee's name, and we'll show you data about those PACs/parties.''')
st.dataframe(filtered_df)
st.write(f'Total rows: {len(filtered_df.index):,}')

if 'TTL_RECEIPTS' in filtered_df.columns:
    st.write(f'Total receipts: ${filtered_df['TTL_RECEIPTS'].sum():,.2f}')
