import pandas as pd
import os

def analiseQuantitiva(filename, colunas):
    print("Gerando arquivos de visualização...")
    try:
        filepath = os.path.join("data", filename)
        df = pd.read_csv(filepath, sep=',', encoding='utf-8')
        
    except FileNotFoundError:
        return f"Erro: O arquivo {filename} não foi encontrado na pasta data/"
    except Exception as e:
        return f"Erro ao processar o arquivo CSV: {str(e)}"

    saida_content = []

    saida_content.append("# Análise Quantitativa de Dados\n")
    saida_content.append("\n")
    saida_content.append("\n")

    saida_content.append("## 1. Análises Quantitativas por Coluna\n")

    for coluna in colunas:
        if coluna not in df.columns:
            saida_content.append(f"### Coluna '{coluna}' não encontrada no arquivo.\n\n")
            continue

        saida_content.append(f"### Análise da Coluna: {coluna}\n")

        # Se for uma coluna de texto, tentamos interpretar como numérica (ex: Idade)
        col = df[coluna]
        numeric_col = None
        if col.dtype == 'object':
            numeric_col = pd.to_numeric(col, errors='coerce')
        elif pd.api.types.is_numeric_dtype(col):
            numeric_col = col

        # Se houver algum valor numérico válido, fazemos análise numérica
        if numeric_col is not None and numeric_col.count() > 0:
            invalid_count = len(col) - numeric_col.count()
            if invalid_count > 0:
                saida_content.append(
                    f"- Nota: {invalid_count} valor(es) não numérico(s) em '{coluna}' foram ignorados/convertidos para NaN.\n"
                )

            saida_content.append("#### Estatísticas Descritivas\n")
            saida_content.append("```\n")
            saida_content.append(numeric_col.describe().to_string())
            saida_content.append("\n```\n\n")
        else:
            # Análise categórica
            saida_content.append("#### Contagem de Valores\n")
            saida_content.append("```\n")
            saida_content.append(col.value_counts().to_string())
            saida_content.append("\n```\n\n")

        # Caso especial para idade
        if coluna.lower() == 'idade':
            idade_numeric = pd.to_numeric(df[coluna], errors='coerce')
            bins = [0, 18, 30, 50, 65, float('inf')]
            labels = ['0-17', '18-29', '30-49', '50-64', '65+']
            faixa_etaria = pd.cut(idade_numeric, bins=bins, labels=labels, right=False)
            contagem_faixa = faixa_etaria.value_counts().sort_index()
            saida_content.append("#### Faixa Etária\n")
            saida_content.append("```\n")
            saida_content.append(contagem_faixa.to_string())
            saida_content.append("\n```\n\n")

    if not df.empty:
        contagem_unica = len(df)
        saida_content.append(f"- **Contagem Única de Registros:** {contagem_unica}\n\n")

    # Garante que a pasta output existe
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "analise-quantitativa.txt")
    with open(output_file, "w", encoding="utf-8") as saida:
        saida.writelines(saida_content)
    
    return f"✓ Análise quantitativa concluída e salva em {output_file}"