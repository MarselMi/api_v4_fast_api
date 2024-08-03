from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper, IncomingTransactionID
from .schemas import CloudPaymentsTransaction, PaySelectionTransaction
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter(tags=["IncomingTransactions"])


# @router.post("/cloud_payments/")
# async def cloud_payments_handler(
#         request: Request,
#         session: Depends(db_helper.scoped_session_dependency),
#         data: CloudPaymentsTransaction
# ):
#     terminal_id: str = request.query_params.get("t")
#     transaction_id = data.TransactionId
#
#     try:
#         it_id = session.query(IncomingTransactionID).filter_by(incoming_id=id).one()
#         return {'code': 0}
#     except NoResultFound:
#         pass
#
#
# @router.post("/pay_selection/")
# async def pay_selection_handler(
#         request: Request,
#         session: Depends(db_helper.scoped_session_dependency),
#         data: PaySelectionTransaction
# ):
#     terminal_id: str = request.query_params.get("t")
