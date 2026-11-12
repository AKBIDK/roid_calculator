from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.project import CostType, BenefitType

class CostBase(BaseModel):
    tipo: CostType
    categoria: str = Field(..., example="Hardware")
    descricao: Optional[str] = None
    valor: float = Field(..., gt=0, example=50000.0)
    ano: int = Field(0, ge=0, example=0)

class CostCreate(CostBase):
    pass

class CostResponse(CostBase):
    id: int
    projeto_id: int

    class Config:
        from_attributes = True

class BenefitBase(BaseModel):
    tipo: BenefitType
    descricao: str = Field(..., example="Redução de horas com automação")
    valor_estimado_anual: float = Field(0.0, ge=0)
    probabilidade_realizacao: float = Field(1.0, ge=0.0, le=1.0, example=0.85)
    ano_inicio: int = Field(1, ge=1)
    ano_fim: int = Field(5, ge=1)

class BenefitCreate(BenefitBase):
    pass

class BenefitResponse(BenefitBase):
    id: int
    projeto_id: int

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    nome: str = Field(..., example="Migração para Cluster Kubernetes com IA")
    descricao: Optional[str] = Field(None, example="Modernização e ganhos operacionais")
    taxa_desconto_anual: float = Field(0.10, ge=0.0, le=1.0, example=0.12)
    vida_util_anos: int = Field(5, ge=1, le=30, example=5)

class ProjectCreate(ProjectBase):
    custos: List[CostCreate] = []
    beneficios: List[BenefitCreate] = []

class ProjectResponse(ProjectBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime
    custos: List[CostResponse] = []
    beneficios: List[BenefitResponse] = []

    class Config:
        from_attributes = True
