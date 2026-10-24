import pandas as pd
import json

arquivo_excel = "Tabelas Equipamentos T20.xlsx"

def limpar_vazios(dicionario):

    item_limpo = {}
    for chave, valor in dicionario.items():
        if pd.isna(valor):
            # Se a célula estiver completamente em branco, atribui texto vazio
            item_limpo[chave] = ""
        else:
            # Se o pandas ler um número inteiro como float (ex: 1.0), converte para inteiro (1)
            if isinstance(valor, float) and valor.is_integer():
                item_limpo[chave] = int(valor)
            else:
                # Transforma qualquer outro dado em texto e remove espaços sobrando nas pontas
                item_limpo[chave] = str(valor).strip()
    return item_limpo

dados = {
    "armas": [limpar_vazios(linha) for linha in pd.read_excel(arquivo_excel, sheet_name="Armas").to_dict('records')],
    "armaduras": [limpar_vazios(linha) for linha in pd.read_excel(arquivo_excel, sheet_name="Armaduras").to_dict('records')],
    "municoes": [limpar_vazios(linha) for linha in pd.read_excel(arquivo_excel, sheet_name="Munições").to_dict('records')]
}

# Converte a estrutura Python para uma string JSON formatada (indent=2 para legibilidade)
# ensure_ascii=False garante que acentos (como ç, ã) não quebrem no código
json_texto = json.dumps(dados, ensure_ascii=False, indent=2)

# Cria e escreve o arquivo .js injetando a variável do banco de dados
with open("equipamentos.js", "w", encoding="utf-8") as arquivo:
    arquivo.write(f"const bdEquipamentos = {json_texto};")

print("Conversão concluída com sucesso! Arquivo equipamentos.js atualizado.")