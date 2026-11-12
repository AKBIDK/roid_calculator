from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.schemas.calculation import ROICalculationResult, MonteCarloRequest, MonteCarloResult
from app.schemas.project import ProjectCreate
from app.services.financial_engine import FinancialEngine
from app.services.monte_carlo import MonteCarloEngine

router = APIRouter(prefix="/api/calculations", tags=["Cálculos Financeiros"])

@router.post("/simulate-instant", response_model=ROICalculationResult)
def simulate_instant(payload: ProjectCreate):
    """
    Calcula instantaneamente o ROI, VPL, TIR e Paybacks para os dados enviados pelo Wizard.
    """
    try:
        custos_dict = [c.model_dump() for c in payload.custos]
        benef_dict = [b.model_dump() for b in payload.beneficios]

        res = FinancialEngine.analyze_project(
            taxa_desconto=payload.taxa_desconto_anual,
            vida_util_anos=payload.vida_util_anos,
            custos=custos_dict,
            beneficios=benef_dict
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no processamento do cálculo: {str(e)}")

@router.post("/monte-carlo", response_model=MonteCarloResult)
def run_monte_carlo(payload: ProjectCreate, config: MonteCarloRequest = Depends()):
    """
    Executa a análise de sensibilidade estocástica via Simulação de Monte Carlo.
    """
    try:
        custos_dict = [c.model_dump() for c in payload.custos]
        benef_dict = [b.model_dump() for b in payload.beneficios]

        sim = MonteCarloEngine.simulate(
            taxa_desconto=payload.taxa_desconto_anual,
            vida_util_anos=payload.vida_util_anos,
            custos=custos_dict,
            beneficios=benef_dict,
            iteracoes=config.iteracoes,
            vol_capex=config.volatilidade_capex,
            vol_opex=config.volatilidade_opex,
            vol_beneficios=config.volatilidade_beneficios,
            vol_tma=config.volatilidade_tma,
            seed=config.seed
        )
        return sim
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Falha na simulação de Monte Carlo: {str(e)}")
