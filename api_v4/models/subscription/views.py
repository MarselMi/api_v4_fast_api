from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import SubscriptionCreate, Subscription, SubscriptionUpdate
from .dependencies import subscription_by_id
from . import crud


router = APIRouter(tags=["Subscriptions"])


@router.get("/", response_model=List[Subscription])
async def get_subscriptions(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_subscriptions(session=session)


@router.post("/", response_model=Subscription, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_in: SubscriptionCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    subscription = await crud.create_subscription(
        session=session, subscription_in=subscription_in
    )
    return subscription


@router.get("/{subscription_id}/", response_model=Subscription)
async def get_subscription(subscription: Subscription = Depends(subscription_by_id)):
    return subscription


@router.patch("/{subscription_id}/", response_model=Subscription)
async def update_subscription(
    subscription_update: SubscriptionUpdate,
    subscription: Subscription = Depends(subscription_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_subscription(
        subscription_update=subscription_update,
        subscription=subscription,
        session=session,
    )
