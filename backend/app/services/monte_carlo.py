"""
Simulação de Sensibilidade e Incerteza (Monte Carlo)
Idealizado por Atena.
Permite simular milhares de cenários estocásticos variando CAPEX, OPEX, taxas e riscos.
"""

import random
import math
from typing import List, Dict, Any, Optional
from app.services.financial_engine import FinancialEngine

class MonteCarloEngine:
    @staticmethod
    def simulate(
        taxa_desconto: float,
        vida_util_anos: int,
        custos: List[Dict[str, Any]],
        beneficios: List[Dict[str, Any]],
        iteracoes: int = 1000,
        vol_capex: float = 0.15,
        vol_opex: float = 0.10,
        vol_beneficios: float = 0.15,
        vol_tma: float = 0.02,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        if seed is not None:
            random.seed(seed)

        vpls: List[float] = []
        tirs: List[float] = []
        paybacks: int = 0

        for _ in range(iteracoes):
            # Variação estocástica com distribuição normal
            fator_capex = max(0.5, random.gauss(1.0, vol_capex))
            fator_opex = max(0.5, random.gauss(1.0, vol_opex))
            fator_benef = max(0.3, random.gauss(1.0, vol_beneficios))
            taxa_sim = max(0.01, random.gauss(taxa_desconto, vol_tma))

            # Custos perturbados
            sim_custos = []
            for c in custos:
                fator = fator_capex if c.get("tipo") in ("CAPEX_INICIAL", "CAPEX") else fator_opex
                sim_custos.append({
                    "tipo": c.get("tipo"),
                    "valor": float(c.get("valor", 0.0)) * fator,
                    "ano": c.get("ano", 0)
                })

            # Benefícios perturbados
            sim_beneficios = []
            for b in beneficios:
                prob = min(1.0, max(0.0, float(b.get("probabilidade_realizacao", 1.0)) * fator_benef))
                sim_beneficios.append({
                    "tipo": b.get("tipo"),
                    "valor_estimado_anual": float(b.get("valor_estimado_anual", 0.0)),
                    "probabilidade_realizacao": prob,
                    "ano_inicio": b.get("ano_inicio", 1),
                    "ano_fim": b.get("ano_fim", vida_util_anos)
                })

            analise = FinancialEngine.analyze_project(taxa_sim, vida_util_anos, sim_custos, sim_beneficios)
            vpls.append(analise["vpl"])
            if analise["tir"] is not None:
                tirs.append(analise["tir"])
            if analise["payback_descontado_anos"] is not None:
                paybacks += 1

        vpls.sort()
        n = len(vpls)

        def percentile(arr, p):
            if not arr:
                return 0.0
            k = (len(arr) - 1) * p
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return arr[int(k)]
            return arr[int(f)] * (c - k) + arr[int(c)] * (k - f)

        vpl_mean = sum(vpls) / n
        vpl_std = math.sqrt(sum((x - vpl_mean) ** 2 for x in vpls) / n)
        prob_sucesso = (sum(1 for x in vpls if x > 0) / n) * 100.0
        prob_payback = (paybacks / n) * 100.0

        tirs.sort()
        tir_percentis = {
            "p10": round(percentile(tirs, 0.10) * 100, 2) if tirs else None,
            "p50": round(percentile(tirs, 0.50) * 100, 2) if tirs else None,
            "p90": round(percentile(tirs, 0.90) * 100, 2) if tirs else None,
        }

        # Construção de histograma com 10 intervalos para o gráfico
        min_v = vpls[0]
        max_v = vpls[-1]
        num_bins = 10
        bin_width = (max_v - min_v) / num_bins if max_v > min_v else 1.0
        bins = [round(min_v + i * bin_width, 2) for i in range(num_bins + 1)]
        counts = [0] * num_bins

        for v in vpls:
            idx = min(int((v - min_v) / bin_width), num_bins - 1)
            counts[idx] += 1

        return {
            "iteracoes": iteracoes,
            "vpl_medio": round(vpl_mean, 2),
            "vpl_desvio_padrao": round(vpl_std, 2),
            "vpl_minimo": round(min_v, 2),
            "vpl_maximo": round(max_v, 2),
            "vpl_percentis": {
                "p10": round(percentile(vpls, 0.10), 2),
                "p25": round(percentile(vpls, 0.25), 2),
                "p50": round(percentile(vpls, 0.50), 2), # Mediana
                "p75": round(percentile(vpls, 0.75), 2),
                "p90": round(percentile(vpls, 0.90), 2)
            },
            "tir_percentis": tir_percentis,
            "probabilidade_vpl_positivo": round(prob_sucesso, 1),
            "probabilidade_payback_atingido": round(prob_payback, 1),
            "histograma": {
                "bins": bins,
                "counts": counts
            }
        }
