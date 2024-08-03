from fastapi import APIRouter

from api_v4.models.incoming_transaction.views import (
    router as incoming_transaction_router,
)

from api_v4.models.partner.views import router as partner_router
from api_v4.models.invoice.views import router as invoice_router
from api_v4.models.manager.views import router as manager_router

from api_v4.models.host.views import router as host_router
from api_v4.models.offer.views import router as offer_router
from api_v4.models.landing.views import router as landing_router
from api_v4.models.prelanding.views import router as prelanding_router
from api_v4.models.landing_element.views import router as land_element_router

from api_v4.models.stream.views import router as stream_router

from api_v4.models.event.views import router as event_router
from api_v4.models.postback.views import router as postback_router
from api_v4.models.acqu_bank.views import router as acqu_bank_router
from api_v4.models.kass_type.views import router as kass_type_router
from api_v4.models.kassa.views import router as kassa_router
from api_v4.models.organisation.views import router as organisation_router
from api_v4.models.paysystem.views import router as pay_system_router
from api_v4.models.transaction_error.views import router as error_router
from api_v4.models.terminal.views import router as terminal_router

from api_v4.models.client.views import router as client_router

from api_v4.statistic.views import router as statistic_router

from api_v4.models.subscription.views import router as subscriptions_router

from api_v4.logging_of_actions.partner_actions.views import (
    router as partner_actions_router,
)
from api_v4.logging_of_actions.operator_actions.views import (
    router as operator_actions_router,
)
from api_v4.logging_of_actions.manager_actions.views import (
    router as manager_actions_router,
)

from api_v4.models.payout_requisite.views import router as payoutrequisites_router

from api_v4.promos.promo.views import router as promo_router


router = APIRouter()
router.include_router(
    router=incoming_transaction_router, prefix="/incomingtransactions"
)

router.include_router(router=partner_router, prefix="/partners")
router.include_router(router=manager_router, prefix="/managers")

router.include_router(router=invoice_router, prefix="/invoices")

router.include_router(router=host_router, prefix="/hosts")
router.include_router(router=offer_router, prefix="/offers")
router.include_router(router=landing_router, prefix="/landings")
router.include_router(router=prelanding_router, prefix="/prelandings")
router.include_router(router=land_element_router, prefix="/landingelements")

router.include_router(router=stream_router, prefix="/streams")

router.include_router(router=event_router, prefix="/events")
router.include_router(router=postback_router, prefix="/postbacks")

router.include_router(router=acqu_bank_router, prefix="/acqubanks")
router.include_router(router=kass_type_router, prefix="/kasstypes")
router.include_router(router=organisation_router, prefix="/organisations")
router.include_router(router=kassa_router, prefix="/kasses")
router.include_router(router=pay_system_router, prefix="/paysystems")
router.include_router(router=error_router, prefix="/transactionerrors")
router.include_router(router=terminal_router, prefix="/terminals")

router.include_router(router=client_router, prefix="/clients")

router.include_router(router=statistic_router, prefix="/statistic")

router.include_router(router=subscriptions_router, prefix="/subscriptions")

router.include_router(router=partner_actions_router, prefix="/partneractions")
router.include_router(router=operator_actions_router, prefix="/operatoractions")
router.include_router(router=manager_actions_router, prefix="/manageractions")

router.include_router(router=payoutrequisites_router, prefix="/payoutrequisites")

router.include_router(router=promo_router, prefix="/promos")
