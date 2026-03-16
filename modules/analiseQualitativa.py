import json
import pandas as pd

def analiseQuantitiva(filename):
    try:
        with open("data/" + filename, "r", encoding="utf-8") as f:
            entrada = json.load(f)
    except FileNotFoundError:
        return f"Erro: O arquivo {filename} não foi encontrado na pasta data/"
    except json.JSONDecodeError:
        return f"Erro: O arquivo {filename} não é um JSON válido."

    df = pd.DataFrame(entrada)
    saida_content = []

    saida_content.append("# Análise Quantitativa de Dados\n")
    saida_content.append("## 1. Lógicas de Agregação de Dados\n")

    # Agregação por Categoria (Soma de Valores) - Exemplo: EstruturaChart.tsx
    if 'estrutura' in df.columns and 'valorProposto' in df.columns:
        agregacao_estrutura = df.groupby('estrutura')['valorProposto'].sum().sort_values(ascending=False)
        saida_content.append("### Agregação por Estrutura (Soma de Valor Proposto)\n")
        saida_content.append("```\n")
        saida_content.append(agregacao_estrutura.to_string())
        saida_content.append("\n```\n\n")

    # Agregação por Frequência (Contagem) - Exemplo: BairrosChart.tsx
    if 'bairro' in df.columns:
        contagem_bairros = df['bairro'].value_counts()
        saida_content.append("### Agregação por Bairro (Contagem de Ocorrências)\n")
        saida_content.append("```\n")
        saida_content.append(contagem_bairros.to_string())
        saida_content.append("\n```\n\n")

    saida_content.append("## 2. Filtros e Categorização Dinâmica\n")

    # Identificação de Emendas Coletivas vs. Individuais
    if 'partido' in df.columns and 'parlamentar' in df.columns and 'valorProposto' in df.columns:
        coletivas = df[df['partido'].str.contains('BANCADA', na=False) |
                       df['parlamentar'].str.lower().str.contains('bancada', na=False) |
                       df['parlamentar'].str.lower().str.contains('comissão', na=False)]
        
        total_valor = df['valorProposto'].sum()
        valor_coletivas = coletivas['valorProposto'].sum()
        
        tipologia_predominante = "Predomínio de emendas individuais"
        if total_valor > 0 and valor_coletivas > total_valor / 2:
            tipologia_predominante = "Predomínio de emendas coletivas"

        saida_content.append("### Análise de Emendas Coletivas vs. Individuais\n")
        saida_content.append(f"- Valor Total de Emendas: R$ {total_valor:,.2f}\n")
        saida_content.append(f"- Valor de Emendas Coletivas: R$ {valor_coletivas:,.2f}\n")
        saida_content.append(f"- Tipologia Predominante: {tipologia_predominante}\n\n")

    saida_content.append("## 3. Métricas de KPI (Indicadores Chave)\n")

    # Total Geral
    if 'valorProposto' in df.columns:
        total_geral = df['valorProposto'].sum()
        saida_content.append(f"- **Total Geral (Valor Proposto):** R$ {total_geral:,.2f}\n")

    # Média por Registro
    if 'valorProposto' in df.columns and not df.empty:
        media_por_registro = df['valorProposto'].mean()
        saida_content.append(f"- **Média por Registro (Valor Proposto):** R$ {media_por_registro:,.2f}\n")

    # Contagem Única (assumindo que cada linha é um registro único ou que há um 'id')
    if not df.empty:
        contagem_unica = len(df)
        saida_content.append(f"- **Contagem Única de Registros:** {contagem_unica}\n\n")

    with open("output/analise.txt", "w", encoding="utf-8") as saida:
        saida.writelines(saida_content)
    
    return "Análise quantitativa concluída e salva em output/analise.txt"

