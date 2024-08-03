from core.models import Invoice
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import InvoiceCreate


async def get_invoices(session: AsyncSession) -> List[Invoice]:
    query = select(Invoice).order_by(Invoice.id)
    result: Result = await session.execute(query)
    invoices = result.scalars().all()
    return list(invoices)


async def get_invoice(session: AsyncSession, invoice_id: int) -> Invoice | None:
    return await session.get(Invoice, invoice_id)


async def create_invoice(session: AsyncSession, invoice_in: InvoiceCreate) -> Invoice:
    invoice_in = invoice_in.model_dump()
    invoice = Invoice(**invoice_in)
    session.add(invoice)
    await session.commit()
    return invoice
