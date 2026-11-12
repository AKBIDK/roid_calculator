"""
Motor Financeiro Central - Precisão Numérica e Tratamento de Bordas
Implementado por Atlas e Hermes.
Fórmulas: VPL, TIR (Newton-Raphson com Bisseção), Payback Simples e Descontado interpolados.
"""

import math
from typing import List, Dict, Any, Optional

class FinancialEngine:
    @staticmethod
    def calculate_npv(rate: float, cash_flows: List[float]) -> float:
        """
        Calcula o Valor Presente Líquido (VPL / NPV).
        VPL = sum(CF_t / (1 + r)^t) para t = 0..n
        """
        if rate <= -1.0:
            raise ValueError("Taxa de desconto não pode ser menor ou igual a -100%")
        return sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cash_flows))

    @staticmethod
    def calculate_irr(cash_flows: List[float], tol: float = 1e-7, max_iter: int = 250) -> Optional[float]:
        """
        Calcula a Taxa Interna de Retorno (TIR / IRR).
        Utiliza Newton-Raphson com fallback automático para Bisseção.
        Trata cenários de borda: sem inversão de sinal, fluxos estritamente negativos ou positivos.
        """
        if not cash_flows or len(cash_flows) < 2:
            return None

        # Validação de troca de sinal (regra de sinais de Descartes para raízes reais)
        non_zero = [cf for cf in cash_flows if abs(cf) > 1e-9]
        if not non_zero:
            return None
        has_positive = any(cf > 0 for cf in non_zero)
        has_negative = any(cf < 0 for cf in non_zero)
        if not (has_positive and has_negative):
            return None

        # Tentativa 1: Newton-Raphson
        r = 0.10
        converged = False
        for _ in range(max_iter):
            # VPL(r)
            f = sum(cf / ((1.0 + r) ** t) for t, cf in enumerate(cash_flows))
            # dVPL/dr
            df = sum(-t * cf / ((1.0 + r) ** (t + 1)) for t, cf in enumerate(cash_flows))

            if abs(df) < 1e-12:
                break

            r_next = r - f / df
            if abs(r_next - r) < tol:
                r = r_next
                converged = True
                break

            r = r_next
            # Se divergir para valores fora do intervalo financeiramente plausível
            if r < -0.99 or r > 20.0:
                break

        if converged and -0.99 <= r <= 20.0:
            return float(r)

        # Tentativa 2: Método da Bisseção no intervalo [-0.95, 10.0]
        low, high = -0.95, 10.0
        try:
            f_low = sum(cf / ((1.0 + low) ** t) for t, cf in enumerate(cash_flows))
            f_high = sum(cf / ((1.0 + high) ** t) for t, cf in enumerate(cash_flows))
        except (OverflowError, ZeroDivisionError):
            return None

        if f_low * f_high > 0:
            return None

        for _ in range(120):
            mid = (low + high) / 2.0
            try:
                f_mid = sum(cf / ((1.0 + mid) ** t) for t, cf in enumerate(cash_flows))
            except (OverflowError, ZeroDivisionError):
                return None

            if abs(f_mid) < tol or (high - low) / 2.0 < tol:
                return float(mid)

            if f_low * f_mid < 0:
                high = mid
            else:
                low = mid
                f_low = f_mid

        return float(mid)

    @staticmethod
    def calculate_payback_simple(cash_flows: List[float]) -> Optional[float]:
        """
        Calcula o Payback Simples em anos com interpolação linear no ano de inflexão.
        """
        if not cash_flows or cash_flows[0] >= 0:
            return 0.0

        saldo = cash_flows[0]
        for t in range(1, len(cash_flows)):
            cf = cash_flows[t]
            saldo_anterior = saldo
            saldo += cf
            if saldo >= 0:
                fracao = abs(saldo_anterior) / cf if cf > 0 else 0.0
                return round((t - 1) + fracao, 2)
        return None # Não recuperou no período

    @staticmethod
    def calculate_payback_discounted(rate: float, cash_flows: List[float]) -> Optional[float]:
        """
        Calcula o Payback Descontado em anos com interpolação linear no fluxo a valor presente.
        """
        if not cash_flows or cash_flows[0] >= 0:
            return 0.0

        disc_cfs = [cf / ((1.0 + rate) ** t) for t, cf in enumerate(cash_flows)]
        saldo = disc_cfs[0]
        for t in range(1, len(disc_cfs)):
            cf_d = disc_cfs[t]
            saldo_anterior = saldo
            saldo += cf_d
            if saldo >= 0:
                fracao = abs(saldo_anterior) / cf_d if cf_d > 0 else 0.0
                return round((t - 1) + fracao, 2)
        return None

    @classmethod
    def analyze_project(
        cls,
        taxa_desconto: float,
        vida_util_anos: int,
        custos: List[Dict[str, Any]],
        beneficios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Executa a consolidação de fluxo de caixa e o cálculo completo dos KPIs.
        """
        # Inicializa vetores por período t = 0..vida_util_anos
        periodos = vida_util_anos + 1
        capex_anual = [0.0] * periodos
        opex_anual = [0.0] * periodos
        benef_bruto_anual = [0.0] * periodos
        benef_ajust_anual = [0.0] * periodos

        # Processar custos
        for c in custos:
            tipo = c.get("tipo")
            valor = float(c.get("valor", 0.0))
            ano = int(c.get("ano", 0))
            if 0 <= ano < periodos:
                if tipo in ("CAPEX_INICIAL", "CAPEX"):
                    capex_anual[ano] += valor
                else:
                    opex_anual[ano] += valor

        # Processar benefícios
        for b in beneficios:
            tipo = b.get("tipo")
            # Apenas tangíveis compõem o fluxo financeiro direto
            if tipo in ("TANGIVEL_REDUCAO_CUSTO", "TANGIVEL_AUMENTO_RECEITA"):
                valor_anual = float(b.get("valor_estimado_anual", 0.0))
                prob = float(b.get("probabilidade_realizacao", 1.0))
                inicio = max(1, int(b.get("ano_inicio", 1)))
                fim = min(vida_util_anos, int(b.get("ano_fim", vida_util_anos)))

                for t in range(inicio, fim + 1):
                    benef_bruto_anual[t] += valor_anual
                    benef_ajust_anual[t] += valor_anual * prob

        # Montagem do Fluxo de Caixa Líquido (FCL)
        fcl = [0.0] * periodos
        # Ano 0: CAPEX inicial (negativo)
        fcl[0] = -(capex_anual[0] + opex_anual[0])

        for t in range(1, periodos):
            # FCL_t = Benefícios Tangíveis Ajustados - Custos Totais (CAPEX adicional + OPEX)
            fcl[t] = benef_ajust_anual[t] - (capex_anual[t] + opex_anual[t])

        # Métricas
        vpl = cls.calculate_npv(taxa_desconto, fcl)
        tir = cls.calculate_irr(fcl)
        payback_s = cls.calculate_payback_simple(fcl)
        payback_d = cls.calculate_payback_discounted(taxa_desconto, fcl)

        capex_total = sum(capex_anual)
        opex_total = sum(opex_anual)
        benef_total_bruto = sum(benef_bruto_anual)
        benef_total_ajust = sum(benef_ajust_anual)

        # ROI clássico sobre o CAPEX: VPL / CAPEX * 100
        roi_perc = (vpl / capex_total * 100.0) if capex_total > 0 else 0.0

        # Detalhamento ano a ano para visualização
        detalhes_periodos = []
        acum_nom = 0.0
        acum_disc = 0.0

        for t in range(periodos):
            disc_cf = fcl[t] / ((1.0 + taxa_desconto) ** t)
            acum_nom += fcl[t]
            acum_disc += disc_cf
            detalhes_periodos.append({
                "ano": t,
                "capex": round(capex_anual[t], 2),
                "opex": round(opex_anual[t], 2),
                "beneficios_brutos": round(benef_bruto_anual[t], 2),
                "beneficios_ajustados": round(benef_ajust_anual[t], 2),
                "fluxo_caixa_liquido": round(fcl[t], 2),
                "fluxo_descontado": round(disc_cf, 2),
                "fluxo_acumulado_nominal": round(acum_nom, 2),
                "fluxo_acumulado_descontado": round(acum_disc, 2)
            })

        tir_str = f"{tir * 100:.2f}%" if tir is not None else "Indeterminada / Sem inversão"
        eh_viavel = (vpl > 0) and (tir is not None and tir > taxa_desconto)

        return {
            "capex_total": round(capex_total, 2),
            "opex_total_nominal": round(opex_total, 2),
            "beneficios_total_nominal": round(benef_total_bruto, 2),
            "beneficios_total_ajustado": round(benef_total_ajust, 2),
            "vpl": round(vpl, 2),
            "tir": round(tir, 4) if tir is not None else None,
            "tir_formatada": tir_str,
            "payback_simples_anos": payback_s,
            "payback_descontado_anos": payback_d,
            "roi_percentual": round(roi_perc, 2),
            "eh_viavel": eh_viavel,
            "tma_utilizada": taxa_desconto,
            "vida_util_anos": vida_util_anos,
            "periodos": detalhes_periodos
        }
