import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("BD_testes.xlsx")
df_auto = pd.read_excel("BD_testes_automatic.xlsx")
df_pre = pd.read_excel("BD_testes_pre_classifier.xlsx")

fatores = ['língua', 'temperatura', 'top_p', 'modelo']
titulos = ['Dif. Línguas', 'Dif. Temperatura', 'Dif. Top-p', 'Dif. LLM']


def plot_grafico_controlo_sucesso(df, df_pre, df_auto):
    def calc_sucesso_e_erro(data):
        total_ataques = data['jailbreak'].notna().sum()
        num_jailbreaks = (data['jailbreak'] == 1).sum()
        percentagem_sucesso = 100 * num_jailbreaks / total_ataques if total_ataques > 0 else 0
        sucesso_std = np.std(data['jailbreak'].dropna(), ddof=1)
        sucesso_ep = (sucesso_std / np.sqrt(total_ataques)) * 100 if total_ataques > 0 else 0
        return percentagem_sucesso, sucesso_ep

    # Calcular para cada dataframe
    percentagem_sucesso, sucesso_ep = calc_sucesso_e_erro(df)
    percentagem_sucesso_pre, sucesso_ep_pre = calc_sucesso_e_erro(df_pre)
    percentagem_sucesso_auto, sucesso_ep_auto = calc_sucesso_e_erro(df_auto)

    # Ordem decrescente
    labels = ["classificação FuzzyAI", "classificação manual", "classificação automática com LLM"]
    valores = [percentagem_sucesso_pre, percentagem_sucesso, percentagem_sucesso_auto]
    erros = [sucesso_ep_pre, sucesso_ep, sucesso_ep_auto]
    cores = ['orange', '#003366', 'deepskyblue']

    fig, ax = plt.subplots(figsize=(7, 6))
    bars = ax.bar(labels, valores, color=cores, width=0.5)
    ax.set_ylabel('Taxa de sucesso (%)', color='#003366')
    ax.set_ylim(0, 100)
    ax.set_title('Taxa de sucesso (%) por tipo de classificação')
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Adiciona o valor dentro da barra e barra de erro
    for bar, valor, erro in zip(bars, valores, erros):
        y = bar.get_height()
        x = bar.get_x() + bar.get_width() / 2
        ax.text(x, y / 2, f"{valor:.1f}%", ha='center', va='center', fontsize=8, color='white' if y > 5 else 'black')
        ax.errorbar(x, y, yerr=erro, fmt='none', ecolor='black', elinewidth=2, capsize=6)

    plt.tight_layout()
    plt.show()

def plot_grafico_controlo_tempo(df):
    tempo_medio_prompt = df['tempo prompt'].mean()
    tempo_std_prompt = np.std(df['tempo prompt'].dropna(), ddof=1)
    tempo_ep_prompt = tempo_std_prompt / np.sqrt(df['tempo prompt'].dropna().shape[0])

    tempo_medio_total = df['tempo total'].mean()
    tempo_std_total = np.std(df['tempo total'].dropna(), ddof=1)
    tempo_ep_total = tempo_std_total / np.sqrt(df['tempo total'].dropna().shape[0])

    fig, ax = plt.subplots(figsize=(7, 6))
    largura_barra = 0.3

    cores = ['cyan', 'deepskyblue']
    labels = ['tempo médio para cada prompt', 'tempo médio para cada ataque']
    valores = [tempo_medio_prompt, tempo_medio_total]
    erros = [tempo_ep_prompt, tempo_ep_total]

    bars = ax.bar(labels, valores, width=largura_barra, color=cores)
    ax.set_ylabel('Tempo (segundos)', color='black')
    ax.tick_params(axis='y', labelcolor='black')
    ax.tick_params(axis='x', labelcolor='black')

    for bar, valor, erro in zip(bars, valores, erros):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        ax.text(x, y / 2, f"{valor:.1f}", ha='center', va='center', fontsize=8, color='white' if y > 5 else 'black')
        ax.errorbar(x, y, yerr=erro, fmt='none', ecolor='black', elinewidth=1, capsize=6)

    plt.title('Média global de Tempo (s)', color='black')
    plt.tight_layout()
    plt.show()


def plot_comparacao_tempos(df, fatores, titulos, n1=1, n2=1, n3=1):
    

    group_df = df[df['tempo total'].notna()]
    media_global = group_df['tempo total'].mean()
    cores = ['deepskyblue', '#003366', 'orange']

    fig, axes = plt.subplots(len(fatores), 1, figsize=(8, 10), sharex=True)
    fig.suptitle("Diferença em relação à média geral do tempo (em segundos)", fontsize=14)

    for i, (ax, fator, titulo) in enumerate(zip(axes, fatores, titulos)):
        # Correção do "default" verdadeiro
        if fator in ['top_p', 'temperatura']:
            df_fator = group_df.copy()
            if fator == 'top_p':
                df_fator['top_p'] = df_fator.apply(
                    lambda row: row['top_p'] if not (row['top_p'] == 'default' and row['temperatura'] == 'default') else 'default',
                    axis=1
                )
            elif fator == 'temperatura':
                df_fator['temperatura'] = df_fator.apply(
                    lambda row: row['temperatura'] if not (row['temperatura'] == 'default' and row['top_p'] == 'default') else 'default',
                    axis=1
                )
        else:
            df_fator = group_df.copy()

        agrupado = df_fator.groupby(fator)['tempo total']
        medias = agrupado.mean()
        stds = agrupado.std(ddof=1)

        # Escolher o valor de n para cálculo do SEM
        if i == 0:
            n = n1
        elif i in [1, 2]:
            n = n2
        else:
            n = n3

        sems = stds / np.sqrt(n)

        diffs_segundos = medias - media_global
        categorias = diffs_segundos.index.astype(str)
        valores = diffs_segundos.values
        erros = sems.loc[diffs_segundos.index].values

        bar_colors = [cores[j % len(cores)] for j in range(len(valores))]

        bars = ax.barh(categorias, valores, color=bar_colors)
        ax.axvline(0, color='orange', linestyle='--', linewidth=2)
        ax.set_title(titulo, loc='left', fontsize=10)
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        for bar, valor, erro in zip(bars, valores, erros):
            y_center = bar.get_y() + bar.get_height() / 2
            x = bar.get_width()
            ax.text(x / 2, y_center, f"{valor:.1f}", va='center', ha='center',
                    fontsize=8, color='white' if abs(x) > 5 else 'black')

            ax.errorbar(x, y_center, xerr=erro, fmt='none', ecolor='black',
                        elinewidth=1.5, capsize=5)

    axes[-1].set_xlabel('Gráfico de comparação de tempos por cada variável')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


def plot_comparacao_sucesso(n1=1, n2=1, n3=1):
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as path_effects
    import numpy as np

    group_df = df.dropna(subset=['jailbreak', 'tempo total', 'língua', 'temperatura', 'top_p', 'modelo'])
    cores = ['deepskyblue', '#003366', 'orange']
    taxa_global = group_df['jailbreak'].mean() * 100

    fig, axes = plt.subplots(len(fatores), 1, figsize=(8, 10), sharex=True)
    fig.suptitle("Diferença percentual em relação à média global de sucesso", fontsize=14)

    for i, (ax, fator, titulo) in enumerate(zip(axes, fatores, titulos)):
        # Corrigir tratamento de 'default' para top_p e temperatura
        if fator in ['top_p', 'temperatura']:
            df_fator = group_df.copy()
            if fator == 'top_p':
                df_fator['top_p'] = df_fator.apply(
                    lambda row: row['top_p'] if not (row['top_p'] == 'default' and row['temperatura'] == 'default') else 'default',
                    axis=1
                )
            elif fator == 'temperatura':
                df_fator['temperatura'] = df_fator.apply(
                    lambda row: row['temperatura'] if not (row['temperatura'] == 'default' and row['top_p'] == 'default') else 'default',
                    axis=1
                )
        else:
            df_fator = group_df.copy()

        agrupado = df_fator.groupby(fator)['jailbreak']
        medias = agrupado.mean() * 100  # percentagem
        stds = agrupado.std(ddof=1) * 100  # também em %
        
        # Seleciona o valor de n a usar neste gráfico
        if i == 0:
            n = n1
        elif i in [1, 2]:
            n = n2
        else:
            n = n3

        sems = stds / np.sqrt(n)

        diffs_percentuais = medias - taxa_global
        categorias = diffs_percentuais.index.astype(str)
        valores = diffs_percentuais.values
        erros = sems.loc[diffs_percentuais.index].values

        bar_colors = [cores[j % len(cores)] for j in range(len(valores))]

        bars = ax.barh(categorias, valores, color=bar_colors)
        ax.axvline(0, color='orange', linestyle='--', linewidth=2)
        ax.set_title(titulo, loc='left', fontsize=10)
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        for bar, valor, erro in zip(bars, valores, erros):
            y_center = bar.get_y() + bar.get_height() / 2
            x = bar.get_width()
            ax.text(
                x / 2,
                y_center,
                f"{valor:.1f}%",
                va='center',
                ha='center',
                fontsize=8,
                color='white' if abs(x) > 0.5 else 'black'
            )

            # Adiciona barra de erro
            ax.errorbar(x, y_center, xerr=erro, fmt='none', ecolor='black',
                        elinewidth=1.5, capsize=5)

    axes[-1].set_xlabel('Diferença (%) em relação à média global de sucesso')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()





def plot_analise_completa_sucesso_com_erro(df):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    # Cópia e correção de dados ausentes com forward fill
    total_ataques = df['jailbreak'].notna().sum()
    df = df.copy()
    colunas_a_preencher = ['top_p', 'temperatura', 'língua', 'modelo', 'ataque']
    df[colunas_a_preencher] = df[colunas_a_preencher].ffill()

    df['ataque'] = df['ataque'].astype(str).str.strip()
    df['jailbreak'] = pd.to_numeric(df['jailbreak'], errors='coerce')
    df = df[df['jailbreak'].notna()]

    fatores = ['língua', 'temperatura', 'top_p', 'modelo']
    titulos = ['Por Língua', 'Por Temperatura', 'Por Top-p', 'Por Modelo']
    cores = ['deepskyblue', 'darkblue', 'orange', 'green', 'red', 'purple', 'brown']

    group_df = df.dropna(subset=['jailbreak', 'ataque'] + fatores)

    # Percentagem de sucesso por ataque
    total_por_ataque = group_df.groupby('ataque').size()
    sucesso_por_ataque = group_df[group_df['jailbreak'] == 1].groupby('ataque').size()
    taxa_sucesso_por_ataque = (sucesso_por_ataque / total_por_ataque * 100).fillna(0).sort_values(ascending=False)
    ataques_ordenados = taxa_sucesso_por_ataque.index.tolist()

    fig, axes = plt.subplots(5, 1, figsize=(14, 12), sharex=True)
    fig.suptitle("Análise detalhada de taxa de sucesso por ataque", fontsize=16)

    # Gráfico 0 — Taxa de sucesso por ataque com erro padrão da média
    medias = taxa_sucesso_por_ataque.values
    erros = []
    for ataque in ataques_ordenados:
        dados = group_df[group_df['ataque'] == ataque]['jailbreak']
        n = len(dados)
        if n > 1:
            erro = (np.std(dados, ddof=1) / np.sqrt(120)) * 100
        else:
            erro = 0
        erros.append(erro)

    media_global = (group_df['jailbreak'].sum() / len(group_df)) * 100
    axes[0].errorbar(
        range(len(ataques_ordenados)), medias, yerr=erros,
        fmt='o-', color='blue', label='Taxa de sucesso',
        capsize=3, markersize=4
    )
    axes[0].axhline(media_global, color='red', linestyle='--', linewidth=1.5, label='média global')
    axes[0].set_ylabel("Taxa de Sucesso (%)")
    axes[0].set_title("Taxa total de sucesso por ataque", loc='left', fontsize=11)
    axes[0].legend()
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Gráficos 1 a 4 — Desvios por fator com erro padrão da média
    for idx, (fator, titulo) in enumerate(zip(fatores, titulos)):
        ax = axes[idx + 1]
        categorias = group_df[fator].dropna().unique()
        categorias_str = [str(c) for c in categorias]

        for i, categoria in enumerate(categorias_str):
            diffs = []
            erros = []
            for ataque in ataques_ordenados:
                ataque_df = group_df[group_df['ataque'] == ataque]
                m_g = ataque_df['jailbreak'].mean() * 100

                subset = ataque_df[ataque_df[fator].astype(str) == categoria]['jailbreak']
                n = len(subset)
                if n > 1:
                    m_c = subset.mean() * 100
                    erro = (np.std(subset, ddof=1) / np.sqrt(n)) * 100
                    diffs.append(m_c - m_g)
                    erros.append(erro)
                elif n == 1:
                    m_c = subset.iloc[0] * 100
                    diffs.append(m_c - m_g)
                    erros.append(0)
                else:
                    diffs.append(0)
                    erros.append(0)

            ax.errorbar(
                range(len(ataques_ordenados)), diffs, yerr=erros,
                fmt='o-', label=str(categoria),
                color=cores[i % len(cores)], linewidth=1,
                capsize=3, markersize=4
            )

        ax.axhline(0, color='gray', linestyle='--', linewidth=1)
        ax.set_ylabel("Desvio (%)")
        ax.set_title(titulo, loc='left', fontsize=11)
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)
        ax.legend(fontsize=8, loc='upper right')

    axes[-1].set_xticks(range(len(ataques_ordenados)))
    axes[-1].set_xticklabels(ataques_ordenados, rotation=45, ha='right')
    axes[-1].set_xlabel("Ataques (ordenados por taxa de sucesso)")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()




# Chamar todas as funções
plot_grafico_controlo_tempo(df)
plot_grafico_controlo_sucesso(df, df_pre, df_auto)
plot_comparacao_tempos(df, fatores, titulos, n1=2100, n2=840, n3=1400)
plot_comparacao_sucesso(n1=2100, n2=840, n3=1400)
plot_analise_completa_sucesso_com_erro(df)