from pydantic import BaseModel
from typing import List, Optional, Dict

class PeriodDetail(BaseModel):
    ano: int
    capex: float
    opex: float
    beneficios_brutos: float
    beneficios_ajustados: float
    fluxo_caixa_liquido: float
    fluxo_descontado: float
    fluxo_acumulado_nominal: float
    fluxo_acumulado_descontado: float

class ROICalculationResult(BaseModel):
    capex_total: float
    opex_total_nominal: float
    beneficios_total_nominal: float
    beneficios_total_ajustado: float
    vpl: float
    tir: Optional[float]
    tir_formatada: str
    payback_simples_anos: Optional[float]
    payback_descontado_anos: Optional[float]
    roi_percentual: float
    eh_viavel: bool
    tma_utilizada: float
    vida_util_anos: int
    periodos: List[PeriodDetail]

class MonteCarloRequest(BaseModel):
    iteracoes: int = 1000
    volatilidade_capex: float = 0.15 # desvio padrão relativo
    volatilidade_opex: float = 0.10
    volatilidade_beneficios: float = 0.15
    volatilidade_tma: float = 0.02
    seed: Optional[int] = None

class MonteCarloResult(BaseModel):
    iteracoes: int
    vpl_medio: float
    vpl_desvio_padrao: float
    vpl_minimo: float
    vpl_maximo: float
    vpl_percentis: Dict[str, float]
    tir_percentis: Dict[str, Optional[float]]
    probabilidade_vpl_positivo: float # em porcentagem
    probabilidade_payback_atingido: float
    histograma: Dict[str, List]
