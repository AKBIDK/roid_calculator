from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class CostType(str, enum.Enum):
    CAPEX_INICIAL = "CAPEX_INICIAL"
    OPEX_RECORRENTE = "OPEX_RECORRENTE"

class BenefitType(str, enum.Enum):
    TANGIVEL_REDUCAO_CUSTO = "TANGIVEL_REDUCAO_CUSTO"
    TANGIVEL_AUMENTO_RECEITA = "TANGIVEL_AUMENTO_RECEITA"
    INTANGIVEL = "INTANGIVEL"

class Project(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    taxa_desconto_anual = Column(Float, nullable=False, default=0.10) # TMA / WACC (ex: 0.10 = 10%)
    vida_util_anos = Column(Integer, nullable=False, default=5)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    custos = relationship("ProjectCost", back_populates="projeto", cascade="all, delete-orphan")
    beneficios = relationship("ProjectBenefit", back_populates="projeto", cascade="all, delete-orphan")
    auditorias = relationship("AuditLog", back_populates="projeto", cascade="all, delete-orphan")

class ProjectCost(Base):
    __tablename__ = "custos_projeto"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    tipo = Column(Enum(CostType), nullable=False)
    categoria = Column(String(100), nullable=False) # Ex: Licenciamento, Hardware, Horas
    descricao = Column(String(255), nullable=True)
    valor = Column(Float, nullable=False)
    ano = Column(Integer, nullable=False, default=0) # 0 para CAPEX inicial, 1..n para OPEX

    projeto = relationship("Project", back_populates="custos")

class ProjectBenefit(Base):
    __tablename__ = "beneficios_projeto"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    tipo = Column(Enum(BenefitType), nullable=False)
    descricao = Column(String(255), nullable=False)
    valor_estimado_anual = Column(Float, nullable=False, default=0.0)
    probabilidade_realizacao = Column(Float, nullable=False, default=1.0) # 0.0 a 1.0 (fator de risco)
    ano_inicio = Column(Integer, nullable=False, default=1)
    ano_fim = Column(Integer, nullable=False, default=5)

    projeto = relationship("Project", back_populates="beneficios")
