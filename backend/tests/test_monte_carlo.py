import unittest
from app.services.monte_carlo import MonteCarloEngine

class TestMonteCarloEngine(unittest.TestCase):
    def test_monte_carlo_distribution(self):
        custos = [{"tipo": "CAPEX_INICIAL", "valor": 100000.0, "ano": 0}]
        beneficios = [{"tipo": "TANGIVEL_REDUCAO_CUSTO", "valor_estimado_anual": 50000.0, "probabilidade_realizacao": 1.0, "ano_inicio": 1, "ano_fim": 3}]

        sim = MonteCarloEngine.simulate(
            taxa_desconto=0.10,
            vida_util_anos=3,
            custos=custos,
            beneficios=beneficios,
            iteracoes=300,
            seed=42
        )
        self.assertEqual(sim["iteracoes"], 300)
        self.assertIn("p10", sim["vpl_percentis"])
        self.assertIn("p50", sim["vpl_percentis"])
        self.assertIn("p90", sim["vpl_percentis"])
        self.assertLess(sim["vpl_percentis"]["p10"], sim["vpl_percentis"]["p90"])
        self.assertTrue(0 <= sim["probabilidade_vpl_positivo"] <= 100)

if __name__ == "__main__":
    unittest.main()
