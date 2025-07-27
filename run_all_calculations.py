# -*- coding: utf-8 -*-
# NOME DO ARQUIVO: run_all_calculations.py

import pandas as pd
import numpy as np
from tqdm import tqdm

# --- Importações das nossas bibliotecas ---
from barrett_scraper_lib import PatientData, BarrettCalculatorScraper
from iol_formulas import IOLFormulas, CONSTANTS

# --- Constantes e Configurações Globais ---
OUTPUT_CSV = 'resultados_consolidados_iol.csv'
A_CONSTANT = 118.99
ASSUMED_ACD = 3.5 # Valor padrão para a fórmula Haigis
FIXED_ELP = 4.0 # Valor padrão para a fórmula Colenbrander
IOL = 'Alcon SN60WF'
EYE = 'R'
N_TESTS = 2

SHORT_EYE_AL = 20.0
SHORT_EYE_K1 = 48
SHORT_EYE_K2 = 46
SHORT_EYE_ACD = 2.8
LONG_EYE_AL = 28.2
LONG_EYE_K1 = 42
LONG_EYE_K2 = 40
LONG_EYE_ACD = 4.5
AL_STEPS = 0.2

def setup_dataframe(test_mode: bool = True):
    """
    Cria e configura o DataFrame com os dados de entrada.
    
    Args:
        test_mode (bool): Se True, gera apenas 2 linhas para teste rápido.
    """
    print("Criando DataFrame com os dados de entrada...")
    
    # --- INÍCIO DA ALTERAÇÃO ---
    # Gera a lista de comprimentos axiais de ... a ... com passos de ...
    axial_lengths = np.arange(SHORT_EYE_AL, LONG_EYE_AL, AL_STEPS)
    num_steps = len(axial_lengths)

    # Gera valores linearmente espaçados para K e ACD
    # K1 vai de ... (para AL min) a ... (para AL max)
    k1_values = np.linspace(SHORT_EYE_K1, LONG_EYE_K1, num=num_steps)
    # K2 vai de ... (para AL min) a ... (para AL max)
    k2_values = np.linspace(SHORT_EYE_K2, LONG_EYE_K2, num=num_steps)
    # ACD vai de ... (para AL min) a ... (para AL max)
    acd_values = np.linspace(SHORT_EYE_ACD, LONG_EYE_ACD, num=num_steps)

    if test_mode:
        # Pega apenas os primeiros N_TESTS itens de cada lista para teste
        axial_lengths = axial_lengths[:N_TESTS]
        # CORREÇÃO: Removido o '1' extra dos nomes das variáveis
        k1_values = k1_values[:N_TESTS]
        k2_values = k2_values[:N_TESTS]
        acd_values = acd_values[:N_TESTS]
        # CORREÇÃO: Mensagem de print melhorada
        print(f">>> MODO DE TESTE ATIVADO: Processando apenas {N_TESTS} linhas. <<<")

    data = {
        'iol_model': [IOL] * len(axial_lengths),
        'a_constant': [A_CONSTANT] * len(axial_lengths),
        'eye_side': [EYE] * len(axial_lengths),
        'axial_length': axial_lengths,
        'meas_k1': k1_values, # Usa os valores que variam linearmente
        'meas_k2': k2_values, # Usa os valores que variam linearmente
        'optical_acd': acd_values, # Usa os valores que variam linearmente
        # 'barrett_universal_ii': [np.nan] * len(axial_lengths) # Coluna renomeada
    }
    
    df = pd.DataFrame(data)
    # --- FIM DA ALTERAÇÃO ---

    # Adiciona colunas vazias para as outras fórmulas
    formula_names = [
        'colenbrander', 'srk', 'hoffer', 'srk_2', 
        'holladay_1', 'hoffer_q', 'srk_t', 'haigis', 'barrett_universal_ii'
    ]
    for name in formula_names:
        df[name] = np.nan

    print("DataFrame criado com sucesso.")
    return df

def run_unified_calculation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Executa o scraper e os cálculos de fórmula para cada linha do DataFrame.
    """
    calculator = IOLFormulas()
    
    print("\nIniciando processo unificado de cálculo...")
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processando Pacientes"):
        
        # --- ETAPA 1: CÁLCULO COM A BIBLIOTECA DE FÓRMULAS ---
        al = row['axial_length']
        k_mean = (row['meas_k1'] + row['meas_k2']) / 2
        corneal_index = CONSTANTS["biometry"]["corneal_index"]
        r = (corneal_index - 1) * 1000 / k_mean
        
        try:
            df.at[index, 'colenbrander'] = calculator.colenbrander_power(al, k_mean, FIXED_ELP)['result']
            df.at[index, 'srk'] = calculator.srk_power(al, k_mean, a_constant=A_CONSTANT)['result']
            df.at[index, 'srk_2'] = calculator.srk_2_power(al, k_mean, a_constant=A_CONSTANT)['result']

            srk_t_elp = calculator._srk_t_elp(al, k_mean, a_constant=A_CONSTANT)['result']
            if not np.isnan(srk_t_elp):
                df.at[index, 'srk_t'] = calculator.srk_t_power(al, k_mean, srk_t_elp)['result']
            hoffer_elp = calculator._hoffer_elp(al, a_constant=A_CONSTANT)['result']
            if not np.isnan(hoffer_elp):
                df.at[index, 'hoffer'] = calculator.hoffer_power(al, k_mean, hoffer_elp)['result']

            holladay_1_elp = calculator._holladay_1_elp(al, k_mean, a_constant=A_CONSTANT)['result']
            if not np.isnan(holladay_1_elp):
                df.at[index, 'holladay_1'] = calculator.holladay_1_power(al, elp=holladay_1_elp, keratometry=k_mean)['result']

            hoffer_q_elp = calculator._hoffer_q_elp(al, k_mean, a_constant=A_CONSTANT)['result']
            if not np.isnan(hoffer_q_elp):
                df.at[index, 'hoffer_q'] = calculator.hoffer_q_power(al, k_mean, hoffer_q_elp)['result']

            haigis_elp = calculator._haigis_elp(al, acd=ASSUMED_ACD, a_constant=A_CONSTANT)['result']
            if not np.isnan(haigis_elp):
                df.at[index, 'haigis'] = calculator.haigis_power(al, r, haigis_elp)['result']

        except Exception as e:
            tqdm.write(f"Erro nas Fórmulas (AL={al}): {e}")
            continue

        # --- ETAPA 2: CÁLCULO COM WEB SCRAPER (Barrett Universal II) ---
        patient_info = PatientData(
            iol_model=row['iol_model'],
            eye_side=row['eye_side'],
            axial_length=row['axial_length'],
            meas_k1=row['meas_k1'],
            meas_k2=row['meas_k2'],
            optical_acd=row['optical_acd']
        )
        
        try:
            with BarrettCalculatorScraper(headless=True) as scraper:
                results_list = scraper.run_calculation(patient_info)

            if results_list and len(results_list) > 3:
                quarto_resultado = results_list[3]
                df.at[index, 'barrett_universal_ii'] = quarto_resultado.iol_power
            else:
                tqdm.write(f"Aviso (Barrett): Não foi possível obter o resultado para AL {row['axial_length']}.")

        except Exception as e:
            tqdm.write(f"Erro no Scraper (AL={row['axial_length']}): {e}")

    return df

def main():
    """Função principal que orquestra todo o processo."""
    # Para rodar o código completo, mude para test_mode=False
    df_inicial = setup_dataframe(test_mode=False)
    
    df_final = run_unified_calculation(df_inicial)
    
    # Arredonda todos os resultados numéricos para 2 casas decimais
    df_final = df_final.round(2)

    try:
        df_final.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
        print(f"\n\nProcesso concluído!")
        print(f"Os resultados foram salvos em '{OUTPUT_CSV}'.")
        print("\n--- Amostra do Resultado Final ---")
        print(df_final.head())
        print("---------------------------------")
    except Exception as e:
        print(f"\nErro ao salvar o arquivo CSV: {e}")

if __name__ == '__main__':
    main()
