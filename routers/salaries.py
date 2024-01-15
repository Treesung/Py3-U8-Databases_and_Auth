from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Salaries
from database import get_db
from .auth import get_current_user

router = APIRouter()


class Salary(BaseModel):
    id: int | None = None
    amount: int
    details: str = Field(min_length=3, max_length=250)
    date_received: datetime = datetime.utcnow()
    is_approved: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 50000,
                "details": "Details of the salary",
                "approved": False
            }
        }


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_salaries(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(Salaries).filter(Salaries.received_by == current_user.get("id")).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_salary(salary_data: Salary, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_salary = Salaries(**salary_data.model_dump(), received_by=current_user.get("id"))

    db.add(new_salary)
    db.commit()


@router.get("/{salary_id}", status_code=status.HTTP_200_OK)
async def get_salary_by_id(salary_id: int = Path(gt=0), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    salary = db.query(Salaries).filter(Salaries.id == salary_id).filter(Salaries.received_by == current_user.get("id")).first()
    if salary is not None:
        return salary
    raise HTTPException(status_code=404, detail=f"Salary with id #{salary_id} was not found")


@router.put("/{salary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_salary_by_id(salary_data: Salary, salary_id: int = Path(gt=0), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    salary = db.query(Salaries).filter(Salaries.id == salary_id).first()

    if salary is None:
        raise HTTPException(status_code=404, detail=f"Salary with id #{salary_id} was not found")

    salary.amount = salary_data.amount
    salary.details = salary_data.details
    salary.is_approved = salary_data.is_approved

    db.add(salary)
    db.commit()


@router.delete("/{salary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_salary_by_id(salary_id: int = Path(gt=0), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    delete_salary = db.query(Salaries).filter(Salaries.id == salary_id).first()

    if delete_salary is None:
        raise HTTPException(status_code=404, detail=f"Salary with id #{salary_id} was not found")

    db.query(Salaries).filter(Salaries.id == salary_id).delete()
    db.commit()