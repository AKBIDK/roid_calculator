#!/usr/bin/env python3
"""
CLI de Demonstração e Teste Rápido do Motor de ROI
Permite testar o motor financeiro e a simulação de Monte Carlo diretamente no terminal.
"""

import sys
from pathlib import Path

# Adiciona o diretório backend ao path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.financial_engine import FinancialEngine
from app.services.monte_carlo import MonteCarloEngine

def main():
    print("=" * 65)
    print("       ROI CALCULATOR - DEMONSTRAÇÃO DO MOTOR FINANCEIRO       ")
    print("=" * 65)

    # Projeto Exemplo: Automação RAG / IA Enterprise
    taxa_desconto = 0.12  # TMA: 12% a.a.
    vida_util_anos = 5

    custos = [
        {"tipo": "CAPEX_INICIAL", "categoria": "Servidores & GPUs", "valor": 120000.0, "ano": 0},
        {"tipo": "CAPEX_INICIAL", "categoria": "Engenharia & Setup", "valor": 60000.0, "ano": 0},
        {"tipo": "OPEX_RECORRENTE", "categoria": "Licenças & APIs", "valor": 25000.0, "ano": 1},
        {"tipo": "OPEX_RECORRENTE", "categoria": "Licenças & APIs", "valor": 25000.0, "ano": 2},
        {"tipo": "OPEX_RECORRENTE", "categoria": "Licenças & APIs", "valor": 25000.0, "ano": 3},
        {"tipo": "OPEX_RECORRENTE", "categoria": "Licenças & APIs", "valor": 25000.0, "ano": 4},
        {"tipo": "OPEX_RECORRENTE", "categoria": "Licenças & APIs", "valor": 25000.0, "ano": 5},
    ]

    beneficios = [
        {
            "tipo": "TANGIVEL_REDUCAO_CUSTO",
            "descricao": "Redução no tempo de suporte N1/N2",
            "valor_estimado_anual": 95000.0,
            "probabilidade_realizacao": 0.85, # 85% de certeza
            "ano_inicio": 1,
            "ano_fim": 5
        },
        {
            "tipo": "TANGIVEL_AUMENTO_RECEITA",
            "descricao": "Retenção de clientes e Upsell",
            "valor_estimado_anual": 30000.0,
            "probabilidade_realizacao": 0.70, # 70% de certeza
            "ano_inicio": 1,
            "ano_fim": 5
        }
    ]

    print("\n[1] Premissas do Projeto:")
    print(f"  - Vida Útil: {vida_util_anos} anos")
    print(f"  - Taxa Mínima de Atratividade (TMA / WACC): {taxa_desconto * 100:.1f}%")
    print(f"  - Investimento Inicial (CAPEX): R$ 180.000,00")
    print(f"  - Custos Recorrentes (OPEX): R$ 25.000,00 / ano")
    print(f"  - Benefício Bruto: R$ 125.000,00 / ano (Ajustado por Risco: R$ 101.750,00 / ano)")

    # 1. Análise Determinística
    analise = FinancialEngine.analyze_project(
        taxa_desconto=taxa_desconto,
        vida_util_anos=vida_util_anos,
        custos=custos,
        beneficios=beneficios
    )

    print("\n[2] Projeção Anual do Fluxo de Caixa (R$):")
    print("-" * 75)
    print(f"{'Ano':<6} | {'CAPEX':<11} | {'OPEX':<10} | {'Ganhos Ponderados':<18} | {'FCL Líquido':<12} | {'Saldo Acum.':<12}")
    print("-" * 75)
    for p in analise["periodos"]:
        print(f"Ano {p['ano']:<2} | {p['capex']:>11,.2f} | {p['opex']:>10,.2f} | {p['beneficios_ajustados']:>18,.2f} | {p['fluxo_caixa_liquido']:>12,.2f} | {p['fluxo_acumulado_descontado']:>12,.2f}")
    print("-" * 75)

    print("\n[3] Indicadores Executivos (KPIs Calculados):")
    print(f"  * Valor Presente Líquido (VPL):       R$ {analise['vpl']:,.2f}")
    print(f"  * Taxa Interna de Retorno (TIR):      {analise['tir_formatada']}")
    print(f"  * Payback Simples:                    {analise['payback_simples_anos']} anos")
    print(f"  * Payback Descontado:                 {analise['payback_descontado_anos']} anos")
    print(f"  * Retorno sobre Investimento (ROI):   {analise['roi_percentual']:.2f}%")
    print(f"  * Parecer do Motor:                  {'[APROVADO] Projeto Viável' if analise['eh_viavel'] else '[REPROVADO] Inviável'}")

    # 2. Simulação de Sensibilidade (Monte Carlo)
    print("\n[4] Análise de Sensibilidade Estocástica (Monte Carlo - 1.000 Simulações):")
    sim = MonteCarloEngine.simulate(
        taxa_desconto=taxa_desconto,
        vida_util_anos=vida_util_anos,
        custos=custos,
        beneficios=beneficios,
        iteracoes=1000,
        seed=42
    )

    print(f"  * Probabilidade de VPL > 0 (Sucesso): {sim['probabilidade_vpl_positivo']:.1f}%")
    print(f"  * Probabilidade de atingir Payback:   {sim['probabilidade_payback_atingido']:.1f}%")
    print(f"  * VPL Cenário Pessimista (P10):       R$ {sim['vpl_percentis']['p10']:,.2f}")
    print(f"  * VPL Cenário Base / Mediana (P50):   R$ {sim['vpl_percentis']['p50']:,.2f}")
    print(f"  * VPL Cenário Otimista (P90):         R$ {sim['vpl_percentis']['p90']:,.2f}")
    print("\n" + "=" * 65 + "\n")

if __name__ == "__main__":
    main()
