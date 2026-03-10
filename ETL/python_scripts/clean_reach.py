import pandas as pd
import os

# ── 1. Perguntar as pastas pelo terminal ─────────────────────────────────────
print("=== LIMPEZA DOS DADOS UFC ===\n")
pasta_origem  = input("Pasta onde estão os CSVs originais: ").strip()
pasta_clean   = input("Pasta de destino para os arquivos limpos (_clean): ").strip()
pasta_removed = input("Pasta de destino para os arquivos removidos (_removed): ").strip()

os.makedirs(pasta_clean,   exist_ok=True)
os.makedirs(pasta_removed, exist_ok=True)

# ── 2. Carregar os CSVs ──────────────────────────────────────────────────────
fighter_tott  = pd.read_csv(os.path.join(pasta_origem, "ufc_fighter_tott.csv"))
fight_stats   = pd.read_csv(os.path.join(pasta_origem, "ufc_fight_stats.csv"))
fight_results = pd.read_csv(os.path.join(pasta_origem, "ufc_fight_results.csv"))

# ── 3. Identificar lutadores SEM reach ──────────────────────────────────────
sem_reach = set(
    fighter_tott[fighter_tott["REACH"].astype(str).str.strip().isin(["--", "", "nan"])]
    ["FIGHTER"]
)

print(f"\nLutadores sem reach encontrados: {len(sem_reach)}")

# ── 4. Remover esses lutadores do fighter_tott ───────────────────────────────
fighter_tott_clean = fighter_tott[~fighter_tott["FIGHTER"].isin(sem_reach)].copy()

# ── 5. Identificar lutas que contêm ao menos um lutador sem reach ────────────
def bout_contem_sem_reach(bout):
    if not isinstance(bout, str):
        return True
    partes = [p.strip() for p in bout.split("vs.")]
    return any(p in sem_reach for p in partes)

lutas_invalidas = fight_results["BOUT"].apply(bout_contem_sem_reach)
bouts_remover   = set(fight_results[lutas_invalidas]["BOUT"])

print(f"Lutas removidas: {lutas_invalidas.sum()}")

# ── 6. Filtrar fight_results e fight_stats ───────────────────────────────────
fight_results_clean = fight_results[~fight_results["BOUT"].isin(bouts_remover)].copy()
fight_stats_clean   = fight_stats[~fight_stats["BOUT"].isin(bouts_remover)].copy()

# ── 7. Separar os dados removidos ───────────────────────────────────────────
fighter_tott_removed  = fighter_tott[fighter_tott["FIGHTER"].isin(sem_reach)].copy()
fight_results_removed = fight_results[fight_results["BOUT"].isin(bouts_remover)].copy()
fight_stats_removed   = fight_stats[fight_stats["BOUT"].isin(bouts_remover)].copy()

# ── 8. Salvar os CSVs limpos ─────────────────────────────────────────────────
fighter_tott_clean.to_csv(os.path.join(pasta_clean, "ufc_fighter_tott_clean.csv"),    index=False)
fight_results_clean.to_csv(os.path.join(pasta_clean, "ufc_fight_results_clean.csv"),  index=False)
fight_stats_clean.to_csv(os.path.join(pasta_clean, "ufc_fight_stats_clean.csv"),      index=False)

# ── 9. Salvar os CSVs com dados removidos ────────────────────────────────────
fighter_tott_removed.to_csv(os.path.join(pasta_removed, "ufc_fighter_tott_removed.csv"),    index=False)
fight_results_removed.to_csv(os.path.join(pasta_removed, "ufc_fight_results_removed.csv"),  index=False)
fight_stats_removed.to_csv(os.path.join(pasta_removed, "ufc_fight_stats_removed.csv"),      index=False)

print("\nArquivos limpos gerados em:", pasta_clean)
print(f"  ufc_fighter_tott_clean.csv   → {len(fighter_tott_clean)} lutadores")
print(f"  ufc_fight_results_clean.csv  → {len(fight_results_clean)} linhas")
print(f"  ufc_fight_stats_clean.csv    → {len(fight_stats_clean)} linhas")

print("\nArquivos de removidos gerados em:", pasta_removed)
print(f"  ufc_fighter_tott_removed.csv   → {len(fighter_tott_removed)} lutadores removidos")
print(f"  ufc_fight_results_removed.csv  → {len(fight_results_removed)} lutas removidas")
print(f"  ufc_fight_stats_removed.csv    → {len(fight_stats_removed)} linhas removidas")