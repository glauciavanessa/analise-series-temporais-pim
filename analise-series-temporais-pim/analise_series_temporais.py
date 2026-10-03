"""Análise de Séries Temporais — Produção Industrial Mensal (PIM-PF)."""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "dados" / "pim.xlsx"
PASTA_GRAFICOS = BASE_DIR / "graficos"
PASTA_GRAFICOS.mkdir(exist_ok=True)

# 1. Importação dos dados
# A planilha deve possuir as colunas Month (data) e Value (valor da PIM).
df = pd.read_excel(ARQUIVO_DADOS)
print("Primeiras observações:")
print(df.head())
print("\nInformações da base:")
df.info()

# 2. Preparação dos dados
# Converte os valores para número; entradas inválidas tornam-se NaN.
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
# Converte a coluna temporal para o tipo de data do pandas.
df["Month"] = pd.to_datetime(df["Month"])
# Ordena cronologicamente para garantir a sequência correta da série.
df = df.sort_values("Month")

# 3. Gráfico da série original
plt.figure(figsize=(12, 5))
plt.plot(df["Month"], df["Value"])
plt.title("Produção Industrial Mensal (PIM-PF)")
plt.xlabel("Mês")
plt.ylabel("PIM")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(PASTA_GRAFICOS / "01_serie_temporal.png", dpi=150)
plt.show()
plt.close()

# 4. A data passa a ser o índice da série temporal.
df = df.set_index("Month")

# 5. Tratamento de valores ausentes por interpolação linear.
df["Value"] = df["Value"].interpolate(method="linear")

# Se ainda existirem valores ausentes nas extremidades, interrompe com aviso.
if df["Value"].isna().any():
    raise ValueError(
        "Ainda existem valores ausentes após a interpolação. "
        "Verifique o início e o fim da planilha."
    )

# 6. Decomposição aditiva
# Como os dados são mensais, period=12 representa um ciclo anual.
decomposicao_aditiva = seasonal_decompose(
    df["Value"], model="additive", period=12
)
fig = decomposicao_aditiva.plot()
fig.set_size_inches(10, 8)
fig.suptitle("Decomposição Aditiva da Série Temporal", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(PASTA_GRAFICOS / "02_decomposicao_aditiva.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close(fig)

# 7. Decomposição multiplicativa
# Este modelo exige valores estritamente positivos.
if (df["Value"] <= 0).any():
    print("\nDecomposição multiplicativa não executada: existem valores <= 0.")
else:
    decomposicao_multiplicativa = seasonal_decompose(
        df["Value"], model="multiplicative", period=12
    )
    fig = decomposicao_multiplicativa.plot()
    fig.set_size_inches(10, 8)
    fig.suptitle("Decomposição Multiplicativa da Série Temporal", fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig(
        PASTA_GRAFICOS / "03_decomposicao_multiplicativa.png",
        dpi=150,
        bbox_inches="tight",
    )
    plt.show()
    plt.close(fig)

print(f"\nAnálise concluída. Gráficos salvos em: {PASTA_GRAFICOS}")
