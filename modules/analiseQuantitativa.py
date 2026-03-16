import pandas as pd
import os

def analiseQuantitiva(filename):
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

    saida_content.append("## 1. Lógicas de Agregação de Dados\n")

    # Agregação por Categoria (Soma de Valores)
    if 'estrutura' in df.columns and 'valorProposto' in df.columns:
        # Convertendo para numérico caso o pandas tenha lido como string
        df['valorProposto'] = pd.to_numeric(df['valorProposto'], errors='coerce').fillna(0)
        
        agregacao_estrutura = df.groupby('estrutura')['valorProposto'].sum().sort_values(ascending=False)
        saida_content.append("### Agregação por Estrutura (Soma de Valor Proposto)\n")
        saida_content.append("```\n")
        saida_content.append(agregacao_estrutura.to_string())
        saida_content.append("\n```\n\n")

    # Agregação por Frequência (Contagem)
    if 'bairro' or 'Bairro' in df.columns:
        contagem_bairros = df['bairro'].value_counts()
        saida_content.append("### Agregação por Bairro (Contagem de Ocorrências)\n")
        saida_content.append("```\n")
        saida_content.append(contagem_bairros.to_string())
        saida_content.append("\n```\n\n")
    
    if 'distrito' or 'Distrito' in df.columns:
        contagem_distritos = df['Distrito'].value_counts()
        saida_content.append("### Agregação por Distrito (Contagem de Ocorrências)\n")
        saida_content.append("```\n")
        saida_content.append(contagem_distritos.to_string())
        saida_content.append("\n```\n\n")

     # Agregação por Escolaridade (Soma de Valores)
   
    if 'sexo' or 'Sexo' in df.columns:
        contagem_sexo = df['Sexo'].value_counts()
        saida_content.append("### Agregação por Sexo (Contagem de Ocorrências)\n")
        saida_content.append("```\n")
        saida_content.append(contagem_sexo.to_string())
        saida_content.append("\n```\n\n")

    if 'idade' or 'Idade' in df.columns:
        df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce')
        bins = [0, 18, 30, 50, 65, float('inf')]
        labels = ['0-17', '18-29', '30-49', '50-64', '65+']
        df['faixa_etaria'] = pd.cut(df['Idade'], bins=bins, labels=labels, right=False)
        contagem_faixa = df['faixa_etaria'].value_counts().sort_index()
        saida_content.append("### Agregação por Faixa Etária (Contagem de Ocorrências)\n")
        saida_content.append("```\n")
        saida_content.append(contagem_faixa.to_string())
        saida_content.append("\n")
        saida_content.append("\n")


    if 'escolaridade' or 'Escolaridade' in df.columns:
        contagem_escolaridade = df['Escolaridade'].value_counts()
        saida_content.append("### Agregação por Escolaridade (Contagem de Ocorrências)\n")
        saida_content.append("```\n")
        saida_content.append(contagem_escolaridade.to_string())
        saida_content.append("\n```\n\n")

    saida_content.append("## 2. Filtros e Categorização Dinâmica\n")

    # Identificação de Emendas Coletivas vs. Individuais
    if 'partido' in df.columns and 'parlamentar' in df.columns and 'valorProposto' in df.columns:
        coletivas = df[df['partido'].astype(str).str.contains('BANCADA', na=False, case=False) |
                       df['parlamentar'].astype(str).str.lower().str.contains('bancada', na=False) |
                       df['parlamentar'].astype(str).str.lower().str.contains('comissão', na=False)]
        
        total_valor = df['valorProposto'].sum()
        valor_coletivas = coletivas['valorProposto'].sum()
        
        tipologia_predominante = "Predomínio de emendas individuais"
        if total_valor > 0 and valor_coletivas > total_valor / 2:
            tipologia_predominante = "Predomínio de emendas coletivas"

        saida_content.append("### Análise de Emendas Coletivas vs. Individuais\n")
        saida_content.append(f"- Valor Total de Emendas: R$ {total_valor:,.2f}\n")
        saida_content.append(f"- Valor de Emendas Coletivas: R$ {valor_coletivas:,.2f}\n")
        saida_content.append(f"- Tipologia Predominante: {tipologia_predominante}\n\n")

    saida_content.append("\n")
    saida_content.append("\n")
    saida_content.append("\n")

    saida_content.append("## 3. Métricas de KPI (Indicadores Chave)\n")

    # Total Geral
    if 'valorProposto' in df.columns:
        total_geral = df['valorProposto'].sum()
        saida_content.append(f"- **Total Geral (Valor Proposto):** R$ {total_geral:,.2f}\n")

    # Média por Registro
    if 'valorProposto' in df.columns and not df.empty:
        media_por_registro = df['valorProposto'].mean()
        saida_content.append(f"- **Média por Registro (Valor Proposto):** R$ {media_por_registro:,.2f}\n")

    # Contagem Única
    if not df.empty:
        contagem_unica = len(df)
        saida_content.append(f"- **Contagem Única de Registros:** {contagem_unica}\n\n")

    # Garante que a pasta output existe
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "analise.txt")
    with open(output_file, "w", encoding="utf-8") as saida:
        saida.writelines(saida_content)
    
    return f"✓ Análise quantitativa concluída e salva em {output_file}"