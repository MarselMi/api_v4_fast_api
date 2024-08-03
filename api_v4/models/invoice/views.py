from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import Invoice, InvoiceCreate
from .dependencies import invoice_by_id
from . import crud

router = APIRouter(tags=["Invoices"])


@router.get("/", response_model=List[Invoice])
async def get_invoice(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_invoices(session=session)


@router.post("/", response_model=Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice(
        invoice_in: InvoiceCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    invoice = await crud.create_invoice(session=session, invoice_in=invoice_in)
    return invoice


@router.get("/{invoice_id}/", response_model=Invoice)
async def get_invoice(
        invoice: Invoice = Depends(invoice_by_id)
):
    return invoice
