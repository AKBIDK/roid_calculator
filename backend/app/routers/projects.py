from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project, ProjectCost, ProjectBenefit
from app.models.audit import AuditLog
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.security import get_current_user, RoleChecker

router = APIRouter(prefix="/api/projects", tags=["Projetos"])

@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db)
):
    proj = Project(
        nome=data.nome,
        descricao=data.descricao,
        taxa_desconto_anual=data.taxa_desconto_anual,
        vida_util_anos=data.vida_util_anos
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)

    for c in data.custos:
        cost = ProjectCost(**c.model_dump(), projeto_id=proj.id)
        db.add(cost)

    for b in data.beneficios:
        benef = ProjectBenefit(**b.model_dump(), projeto_id=proj.id)
        db.add(benef)

    # Log de auditoria (Têmis Compliance)
    audit = AuditLog(
        projeto_id=proj.id,
        usuario="sistema",
        acao="CRIACAO_PROJETO",
        detalhes=f"Criado projeto '{proj.nome}' com taxa {proj.taxa_desconto_anual*100}%"
    )
    db.add(audit)
    db.commit()
    db.refresh(proj)
    return proj
