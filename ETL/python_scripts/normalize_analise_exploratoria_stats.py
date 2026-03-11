import pandas as pd
import os

# ── 1. Perguntar as pastas pelo terminal ─────────────────────────────────────
print("=== TRANSFORMAÇÃO DO UFC FIGHT STATS ===\n")
pasta_origem = input("Pasta onde está o ufc_fight_stats_clean.csv: ").strip()
pasta_saida  = input("Pasta de destino para o arquivo transformado: ").strip()

os.makedirs(pasta_saida, exist_ok=True)

df = pd.read_csv(os.path.join(pasta_origem, "ufc_fight_stats_clean.csv"))

# ── 2. Função para separar "X of Y" ─────────────────────────────────────────
def separar_x_of_y(serie):
    landed   = []
    attempted = []
    for val in serie:
        try:
            partes = str(val).strip().split(" of ")
            landed.append(int(partes[0]))
            attempted.append(int(partes[1]))
        except:
            landed.append(None)
            attempted.append(None)
    return landed, attempted

# ── 3. Função para limpar percentual "61%" ou "---" ─────────────────────────
def limpar_pct(serie):
    valores = []
    for val in serie:
        try:
            v = str(val).strip().replace("%", "")
            valores.append(None if v in ["---", ""] else float(v))
        except:
            valores.append(None)
    return valores

# ── 4. Separar cada campo ────────────────────────────────────────────────────
sig_landed,   sig_attempted   = separar_x_of_y(df["SIG.STR."])
total_landed, total_attempted = separar_x_of_y(df["TOTAL STR."])
td_landed,    td_attempted    = separar_x_of_y(df["TD"])

sig_pct = limpar_pct(df["SIG.STR. %"])
td_pct  = limpar_pct(df["TD %"])

# ── 5. Montar novo dataframe ─────────────────────────────────────────────────
df_novo = pd.DataFrame({
    "EVENT":                df["EVENT"],
    "BOUT":                 df["BOUT"],
    "ROUND":                df["ROUND"],
    "FIGHTER":              df["FIGHTER"],
    "SIG.STR. LANDED":      sig_landed,
    "SIG.STR. ATTEMPTED":   sig_attempted,
    "SIG.STR. %":           sig_pct,
    "TOTAL STR. LANDED":    total_landed,
    "TOTAL STR. ATTEMPTED": total_attempted,
    "TD LANDED":            td_landed,
    "TD ATTEMPTED":         td_attempted,
    "TD %":                 td_pct,
})

# ── 6. Salvar ────────────────────────────────────────────────────────────────
saida = os.path.join(pasta_saida, "ufc_fight_stats_transformed.csv")
df_novo.to_csv(saida, index=False)

print(f"\nArquivo gerado: {saida}")
print(f"Total de registros: {len(df_novo)}")
print(f"\nColunas geradas:")
for col in df_novo.columns:
    print(f"  {col}")