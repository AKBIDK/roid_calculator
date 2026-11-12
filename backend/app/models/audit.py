from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=True)
    usuario = Column(String(100), nullable=False, default="sistema")
    acao = Column(String(100), nullable=False) # CRIACAO, ATUALIZACAO_PREMISSAS, CALCULO_ROI
    detalhes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    projeto = relationship("Project", back_populates="auditorias")
