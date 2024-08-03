from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Partner

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


async def generate_partner_uid(
        partner_id: int, session: AsyncSession, alphabet: str = BASE62
):
    num = partner_id * 100
    if num == 0:
        return alphabet[0]
    arr = []
    arr_append = arr.append
    _divmod = divmod
    base = len(alphabet)
    while num:
        num, rem = _divmod(num, base)
        arr_append(alphabet[rem])
    arr.reverse()
    res = "".join(arr)
    partner = await session.get(Partner, partner_id)
    partner.uid = res
    await session.commit()
    return partner
