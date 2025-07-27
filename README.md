# Calculadora de Lentes Intraoculares (LIO)

Este projeto automatiza o cálculo da potência de lentes intraoculares (LIO) usando diversas fórmulas, incluindo a extração de dados da fórmula de Barrett Universal II através de web scraping.

## Funcionalidades

*   Calcula a potência da LIO usando as seguintes fórmulas:
    *   Colenbrander
    *   SRK
    *   Hoffer
    *   SRK II
    *   Holladay 1
    *   Hoffer Q
    *   SRK/T
    *   Haigis
*   Extrai o resultado da fórmula Barrett Universal II do site [APACRS](https://calc.apacrs.org/barrett_universal2105/).
*   Gera um arquivo CSV (`resultados_consolidados_iol.csv`) com os resultados de todas as fórmulas para uma faixa de comprimentos axiais.
*   Cria um gráfico interativo (`grafico_comparativo_formulas.html`) para visualizar e comparar os resultados.

## Como Usar

### 1. Instalação

Clone o repositório e instale as dependências:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd selenium-iol-calc
pip install -r requirements.txt
```

### 2. Execução

Para executar todos os cálculos e gerar o gráfico, execute o script principal:

```bash
python run_all_calculations.py
```

Isso irá:
1.  Gerar o arquivo `resultados_consolidados_iol.csv` com os dados.
2.  Em seguida, você pode gerar o gráfico interativo executando:

```bash
python generate_interactive_chart.py
```

O gráfico será salvo como `grafico_comparativo_formulas.html`.

### 3. Visualização

Abra o arquivo `grafico_comparativo_formulas.html` em seu navegador para ver o gráfico interativo.

## Arquivos do Projeto

*   `run_all_calculations.py`: Script principal que orquestra os cálculos.
*   `iol_formulas.py`: Biblioteca com a implementação das fórmulas de LIO.
*   `barrett_scraper_lib.py`: Biblioteca para fazer o web scraping da calculadora Barrett.
*   `generate_interactive_chart.py`: Script para gerar o gráfico comparativo.
*   `requirements.txt`: Lista de dependências do Python.
*   `resultados_consolidados_iol.csv`: Arquivo de saída com os resultados.
*   `grafico_comparativo_formulas.html`: Arquivo de saída com o gráfico.
