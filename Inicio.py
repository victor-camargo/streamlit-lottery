import streamlit as st
import pandas as pd
from itertools import combinations
from random import sample


def check_tenth():
    if st.session_state['first-tenth'] >= st.session_state['last-tenth']:

        st.session_state['first-tenth'] = st.session_state['first-tenth-last-state']
        st.session_state['last-tenth'] = st.session_state['last-tenth-last-state']
        
def sort_removed_tenths():
    st.session_state['removed-tenth'] = sorted(st.session_state['removed-tenth'])

def sort_fixed_tenths():
    st.session_state['fixed-tenth'] = sorted(st.session_state['fixed-tenth'])

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


st.title("Aplicação loteria")

col1, col2 = st.columns(2)

with col1:
    
    st.number_input("Insira a primeira dezena", value = 1, key='first-tenth', on_change=check_tenth)
    st.session_state['first-tenth-last-state'] = st.session_state['first-tenth']
with col2:
    st.number_input("Insira a última dezena", value = 25, key='last-tenth', on_change=check_tenth)
    st.session_state['last-tenth-last-state'] = st.session_state['last-tenth']

    
st.session_state['available-tenth'] = list(range(st.session_state['first-tenth'], st.session_state['last-tenth']+1))


st.text('Dezenas disponíveis:\n' + str(st.session_state['available-tenth']))



with st.container():
    st.header("Retirar dezenas")
    to_remove = st.multiselect("Selecione as dezenas que deseja deixar de fora:",
                   options = st.session_state['available-tenth'],
                   key='removed-tenth',
                   on_change = sort_removed_tenths)

    
    st.session_state['after-removed-tenth'] = [x for x in st.session_state['available-tenth'] if x not in to_remove]
    
    
        
    st.text('Dezenas disponíveis após retirar dezenas:\n' + str(st.session_state['after-removed-tenth']))


with st.container():
    st.header("Fixar dezenas")
    to_fix = st.multiselect("Selecione as dezenas que deseja fixar nas combinações:",
                   options = st.session_state['after-removed-tenth'],
                   key='fixed-tenth',
                   on_change = sort_fixed_tenths )  

    
    st.session_state['available-use-tenth'] = [x for x in st.session_state['after-removed-tenth'] if x not in to_fix]

    st.text('Dezenas disponíveis para combinar após fixar dezenas desejadas:\n' + str(st.session_state['available-use-tenth']))

with st.container():
    st.header("Combinar dezenas")

    st.text("Dezenas disponíveis para sortear: \n" + str(st.session_state['available-use-tenth']))
    
    n_combs = st.selectbox("Quantos dezenas deseja sortear dentro das dezenas acima?:",
                          options = list(range(len(st.session_state['available-use-tenth']) +1)))

    combs = combinations(st.session_state['available-use-tenth'], n_combs)

    resultados = []

    for comb in combs:
        resultados.append(sorted(st.session_state['fixed-tenth'] + list(comb)))

    df = pd.DataFrame(resultados)
    csv = convert_df(df)

    

    if len(resultados) <= 100000:
        st.subheader("Combinações finais")
        st.dataframe(df)
    else:
        st.subheader("Primeiras 50 combinações")
        st.dataframe(df.head(50))
        st.subheader("Últimas 50 combinações")
        st.dataframe(df.tail(50))

    st.subheader("Foram gerados ao todo {} combinações de {} dezenas, utilizando as seguintes configurações:".format(len(resultados), n_combs + len(st.session_state['fixed-tenth'])))
    st.subheader("Dezenas disponíveis para combinar: {}".format(tuple(st.session_state['available-use-tenth'])))
    st.subheader("Dezenas fixadas: {}".format(tuple(st.session_state['fixed-tenth'])))
    st.download_button("Baixar arquivo combinações",csv, "file.csv", "text/csv", key='download-csv')

    
    
with st.container():
    st.header("Sortear combinações aleatoriamente")

    n_random = st.selectbox("Quantos dezenas deseja sortear aleatoriamente, dentro das combinações geradas?",
                          options = list(range(1,len(resultados) +1)))

    rand_sample_combs = sample(resultados, n_random)

    df_rand = pd.DataFrame(rand_sample_combs)
    csv_rand = convert_df(df_rand)
    
    if len(rand_sample_combs) <= 100000:
        st.subheader("Combinações finais")
        st.dataframe(df_rand)
    else:
        st.subheader("Primeiras 50 combinações")
        st.dataframe(df_rand.head(50))
        st.subheader("Últimas 50 combinações")
        st.dataframe(df_rand.tail(50))

    st.download_button("Baixar arquivo combinações aleatórias",csv_rand, "file_rand.csv", "text/csv", key='download-csv-rand')
    
