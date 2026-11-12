import unittest
from app.services.financial_engine import FinancialEngine

class TestFinancialEngine(unittest.TestCase):
    def test_npv_standard(self):
        # Fluxo clássico: -100k, 30k, 40k, 50k, 40k a 10%
        cfs = [-100000.0, 30000.0, 40000.0, 50000.0, 40000.0]
        npv = FinancialEngine.calculate_npv(0.10, cfs)
        self.assertAlmostEqual(npv, 25216.86, places=2)

    def test_irr_standard(self):
        cfs = [-100000.0, 30000.0, 40000.0, 50000.0, 40000.0]
        irr = FinancialEngine.calculate_irr(cfs)
        self.assertIsNotNone(irr)
        self.assertAlmostEqual(irr, 0.20496, places=4)

    def test_irr_edge_case_no_sign_change(self):
        # Todos positivos ou todos negativos (sem inversão) -> deve retornar None
        all_neg = [-100.0, -50.0, -30.0]
        all_pos = [100.0, 200.0, 300.0]
        self.assertIsNone(FinancialEngine.calculate_irr(all_neg))
        self.assertIsNone(FinancialEngine.calculate_irr(all_pos))

    def test_payback_simple_interpolation(self):
        # -100k, 30k (saldo -70k), 40k (saldo -30k), 50k (saldo +20k) -> 2 + 30/50 = 2.6 anos
        cfs = [-100000.0, 30000.0, 40000.0, 50000.0, 40000.0]
        payback = FinancialEngine.calculate_payback_simple(cfs)
        self.assertEqual(payback, 2.6)

    def test_payback_discounted_interpolation(self):
        cfs = [-100000.0, 30000.0, 40000.0, 50000.0, 40000.0]
        payback_d = FinancialEngine.calculate_payback_discounted(0.10, cfs)
        self.assertAlmostEqual(payback_d, 3.08, places=2)

    def test_payback_never_recovers(self):
        # Investimento não recuperado no ciclo de vida
        cfs = [-100000.0, 10000.0, 10000.0, 10000.0]
        self.assertIsNone(FinancialEngine.calculate_payback_simple(cfs))
        self.assertIsNone(FinancialEngine.calculate_payback_discounted(0.10, cfs))

    def test_full_project_analysis(self):
        custos = [
            {"tipo": "CAPEX_INICIAL", "categoria": "Hardware", "valor": 100000.0, "ano": 0},
            {"tipo": "OPEX_RECORRENTE", "categoria": "Manutenção", "valor": 10000.0, "ano": 1},
            {"tipo": "OPEX_RECORRENTE", "categoria": "Manutenção", "valor": 10000.0, "ano": 2},
            {"tipo": "OPEX_RECORRENTE", "categoria": "Manutenção", "valor": 10000.0, "ano": 3},
        ]
        beneficios = [
            {"tipo": "TANGIVEL_REDUCAO_CUSTO", "valor_estimado_anual": 50000.0, "probabilidade_realizacao": 0.90, "ano_inicio": 1, "ano_fim": 3}
        ]
        # Benefício líquido por ano = 50.000 * 0.9 - 10.000 = 35.000
        # FCL: [-100000, 35000, 35000, 35000]
        res = FinancialEngine.analyze_project(taxa_desconto=0.10, vida_util_anos=3, custos=custos, beneficios=beneficios)
        self.assertEqual(res["capex_total"], 100000.0)
        self.assertEqual(res["opex_total_nominal"], 30000.0)
        self.assertGreater(res["vpl"], -20000.0) # VPL em torno de -12.960
        self.assertFalse(res["eh_viavel"])

if __name__ == "__main__":
    unittest.main()
