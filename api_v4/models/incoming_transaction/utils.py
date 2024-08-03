from datetime import datetime, timedelta
from core.models import Subscription, Transaction, Terminal, PostbackEvent, Offer, Check

from uuid import uuid4


class IncomingTransactionHandler:

    def __init__(self, session, terminal_id, data):
        self.session = session
        self.terminal_id = terminal_id
        self.data = data

    def cloud_payments(self):
        pass

    def pay_selection(self):
        pass

    async def activate_subscription(self, transaction, pk):
        subscription = await self.session.query(Subscription).filter_by(id=pk).first()

        partner = subscription.client.host.partner
        offer = subscription.client.offer
        host = subscription.client.host

        await self.generate_postback(host, transaction, event='subscribe', sub=subscription)

        if offer.subs_pay == 1:
            if partner.permanent == 0 and partner.temporary_end <= datetime.now().date() <= partner.temporary_start.date():
                new_transaction = Transaction(
                    sum=(transaction.amount * partner.temporary_percent) / 100,
                    direction=1,
                    partner=partner,
                    host=host,
                    incoming_transaction=transaction,
                    percent=partner.temporary_percent,
                    create_date_hour=datetime.now().hour,
                    n_terminal_id=transaction.n_terminal_id
                )
                self.session.add(new_transaction)
                await self.session.commit()
                subscription.profit += new_transaction.sum
                await self.session.commit()
                if partner.referal:
                    new_referal_transaction = Transaction(
                        sum=(
                                    (
                                            transaction.amount * partner.temporary_percent
                                    ) / 100 * partner.referal.referal_fees
                            ) / 100,
                        direction=1,
                        partner=partner.referal,
                        host=host,
                        incoming_transaction=transaction,
                        ref=partner,
                        ref_transaction=True,
                        percent=partner.referal.referal_fees,
                        create_date_hour=datetime.now().hour,
                        n_terminal_id=transaction.n_terminal_id
                    )
                    self.session.add(new_referal_transaction)
                    await self.session.commit()
            else:
                partner.permanent = 1
                await self.session.commit()
                new_transaction = Transaction(
                    sum=(transaction.amount * partner.percent) / 100,
                    direction=1,
                    partner=partner,
                    host=host,
                    incoming_transaction=transaction,
                    create_date_hour=datetime.now().hour,
                    n_terminal_id=transaction.n_terminal_id
                )
                self.session.add(new_transaction)
                await self.session.commit()
                subscription.profit += new_transaction.sum
                await self.session.commit()
                if partner.referal:
                    new_referal_transaction = Transaction(
                        sum=(((transaction.amount * partner.percent) / 100) * partner.referal.referal_fees) / 100,
                        direction=1,
                        partner=partner.referal,
                        host=host,
                        incoming_transaction=transaction,
                        ref=partner,
                        ref_transaction=True,
                        percent=partner.referal.referal_fees,
                        create_date_hour=datetime.now().hour,
                        n_terminal_id=transaction.n_terminal_id
                    )
                    self.session.add(new_referal_transaction)
                    await self.session.commit()

        if offer.author_pay == 1:
            manager = offer.manager
            new_transaction = Transaction(
                sum=(transaction.amount * offer.author_percent) / 100,
                direction=1,
                manager=manager,
                host=host,
                incoming_transaction=transaction,
                percent=offer.author_percent,
                create_date_hour=datetime.now().hour,
                n_terminal_id=transaction.n_terminal_id
            )
            self.session.add(new_transaction)
            await self.session.commit()

        terminal = await self.session.query(Terminal).filter_by(id=transaction.n_terminal_id).first()

        if subscription.type == 'height':
            subscription.status = 'ACTIVE'
            subscription.start_date = datetime.now()
            subscription.start_date_day = datetime.now().date()
            subscription.start_date_hour = datetime.now().hour
            subscription.is_start = 1
            subscription.pay_date = datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))
            subscription.pay_date_day = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).date()
            subscription.pay_date_hour = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).hour
            subscription.two_pay_date = datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))
            subscription.two_pay_date_day = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).date()
            subscription.two_pay_date_hour = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).hour
            subscription.card_number = transaction.card_first_six + 'xxxxx' + transaction.card_last_four
            subscription.token = transaction.token
            subscription.transaction_id = transaction
            subscription.n_terminal_id = transaction.n_terminal_id
            subscription.terminal_id = terminal
        elif subscription.type == 'lower':
            subscription.status = 'ACTIVE'
            subscription.start_date = datetime.now()
            subscription.start_date_day = datetime.now().date()
            subscription.start_date_hour = datetime.now().hour
            subscription.is_start = 1
            subscription.pay_date = datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))
            subscription.pay_date_day = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).date()
            subscription.pay_date_hour = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).hour
            subscription.two_pay_date = datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))
            subscription.two_pay_date_day = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).date()
            subscription.two_pay_date_hour = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).hour
            subscription.card_number = transaction.card_first_six + 'xxxxx' + transaction.card_last_four
            subscription.token = transaction.token
            subscription.transaction_id = transaction
            subscription.n_terminal_id = transaction.n_terminal_id
            subscription.terminal_id = terminal
        else:
            subscription.status = 'ACTIVE'
            subscription.start_date = datetime.now()
            subscription.start_date_day = datetime.now().date()
            subscription.start_date_hour = datetime.now().hour
            subscription.is_start = 1
            subscription.pay_date = datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))
            subscription.pay_date_day = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).date()
            subscription.pay_date_hour = (
                    datetime.now() + timedelta(seconds=(subscription.freeday * 24 * 60 * 60))).hour
            subscription.card_number = transaction.card_first_six + 'xxxxx' + transaction.card_last_four
            subscription.token = transaction.token
            subscription.transaction_id = transaction
            subscription.n_terminal_id = transaction.n_terminal_id
            subscription.terminal_id = terminal

        client = subscription.client
        client.card_first_six = transaction.card_first_six
        client.card_last_four = transaction.card_last_four
        await self.session.commit()

        await self.check_kass(transaction, client)

        if not client.first_subscribe:
            client.first_subscribe = datetime.now()
            client.first_subscribe_day = datetime.now().date()
            client.first_subscribe_hour = datetime.now().hour
            client.active = 1
            await self.session.commit()
            await self.generate_postback(host=host, event='activate', sub=subscription)

    async def renew_subscription(self, transaction, pk):
        subscription = await self.session.query(Subscription).filter_by(pk=pk).first()
        if not subscription:
            raise ValueError("Subscription not found")

        current_time = datetime.now()
        new_pay_date = subscription.pay_date + timedelta(days=subscription.period) \
            if subscription.pay_date > current_time \
            else current_time + timedelta(days=subscription.period)
        two_new_pay_date = subscription.pay_date + timedelta(days=subscription.two_period) \
            if subscription.two_period else None

        host = subscription.client_id.host_id
        offer = subscription.client_id.offer_id
        partner = subscription.client_id.host_id.partner_id

        if partner.permanent == 0:
            if partner.temporary_end.date() <= datetime.now().date() <= partner.temporary_start.date():
                partner_percent = partner.temporary_percent
            else:
                partner_percent = partner.percent

            new_transaction = Transaction(
                sum=(transaction.amount * partner_percent) / 100,
                direction=1,
                partner_id=partner,
                host_id=host,
                incoming_transaction_id=transaction,
                percent=partner_percent,
                time=datetime.now(),
                create_date_day=datetime.now().date(),
                create_date_hour=datetime.now().hour,
                n_terminal_id=transaction.n_terminal_id
            )
            self.session.add(new_transaction)
            subscription.profit += new_transaction.sum
            await self.generate_postback(host, new_transaction, 'rebill', subscription)

        else:
            partner.permanent = 1
            self.session.add(partner)
            await self.session.commit()

            new_transaction = Transaction(
                sum=(transaction.amount * partner.percent) / 100,
                direction=1,
                partner_id=partner,
                host_id=host,
                incoming_transaction_id=transaction,
                percent=partner.percent,
                time=datetime.now(),
                create_date_day=datetime.now().date(),
                create_date_hour=datetime.now().hour,
                n_terminal_id=transaction.n_terminal_id
            )
            self.session.add(new_transaction)
            subscription.profit += new_transaction.sum
            await self.generate_postback(host, new_transaction, 'rebill', subscription)

        if offer.author_pay == 1:
            manager = offer.manager_id
            new_manager_transaction = Transaction(
                sum=(transaction.amount * offer.author_percent) / 100,
                direction=1,
                manager_id=manager,
                host_id=host,
                incoming_transaction_id=transaction,
                percent=offer.author_percent,
                time=datetime.now(),
                create_date_day=datetime.now().date(),
                create_date_hour=datetime.now().hour,
                n_terminal_id=transaction.n_terminal_id
            )
            self.session.add(new_manager_transaction)

        if partner.referal:
            partner_percent = partner.temporary_percent if partner.permanent == 0 else partner.percent
            referal_fees = partner.referal.referal_fees
            new_referal_transaction = Transaction(
                sum=((transaction.amount * partner_percent) / 100) * referal_fees / 100,
                direction=1,
                partner_id=partner.referal,
                host_id=host,
                incoming_transaction_id=transaction,
                ref=partner,
                ref_transaction=True,
                percent=referal_fees,
                time=datetime.now(),
                create_date_day=datetime.now().date(),
                create_date_hour=datetime.now().hour,
                n_terminal_id=transaction.n_terminal_id
            )
            self.session.add(new_referal_transaction)

        if subscription.type in ['height', 'lower'] and subscription.two_tarif_sum == transaction.amount:
            pay_date = two_new_pay_date if two_new_pay_date else new_pay_date
        else:
            pay_date = new_pay_date

        subscription.pay_date = pay_date
        subscription.pay_date_day = pay_date.date()
        subscription.pay_date_hour = pay_date.hour
        subscription.card_number = transaction.card_first_six + 'xxxxx' + transaction.card_last_four
        subscription.transaction_id = transaction
        subscription.count_good += 1
        subscription.try_count = 0

        client = subscription.client_id
        client.card_first_six = transaction.card_first_six
        client.card_last_four = transaction.card_last_four

        self.session.add(subscription)
        self.session.add(client)
        await self.session.commit()

        await self.check_kass(transaction, client)

    async def bad_rebill(self, transaction, pk):
        subscription = await self.session.query(Subscription).filter_by(pk=pk).first()

        if not subscription:
            return

        partner = subscription.client.host.partner
        offer = subscription.client.offer
        host = subscription.client.host

        if transaction.amount >= 100:
            try_count = subscription.try_count + 1 if subscription.try_count else 1
            count_fail = subscription.count_fail + 1 if subscription.count_fail else 1

            if subscription.type in ['height', 'lower']:
                subscription.two_try_date = datetime.now()
                subscription.two_try_date_day = datetime.now().date()
                subscription.two_try_date_hour = datetime.now().hour
            else:
                subscription.try_date = datetime.now()
                subscription.try_date_day = datetime.now().date()
                subscription.try_date_hour = datetime.now().hour

            subscription.try_count = try_count
            subscription.count_fail = count_fail
            subscription.transaction = transaction

        else:
            terminal = await self.session.query(Terminal).filter_by(id=transaction.n_terminal_id).first()

            subscription.transaction = transaction
            subscription.n_terminal_id = transaction.n_terminal_id
            subscription.terminal = terminal

        await self.session.commit()

    async def generate_postback(self, host, transaction=None, event='', sub=None):
        transaction_id = str(uuid4())
        sum_ = transaction.sum if transaction else None

        postback_data = {
            'stream_id': host.stream_id,
            'payout': sum_,
            'transaction_id': transaction_id,
            'type': event,
            'partner_id': host.partner_id,
            'offer_id': host.landing_id.offer_id,
            'landing_id': host.landing_id,
            'status': 'NO_PROCESS',
            'utm_source': host.utm_source,
            'utm_medium': host.utm_medium,
            'utm_campaign': host.utm_campaign,
            'utm_content': host.utm_content,
            'utm_term': host.utm_term,
            'sub_1': host.sub_1,
            'sub_2': host.sub_2,
            'sub_3': host.sub_3,
            'sub_4': host.sub_4,
            'sub_5': host.sub_5,
            'click_id': host.click_id,
        }

        if sub:
            postback_data.update({
                'n_subscription_id': sub.pk,
                'n_client_id': sub.client_id.pk,
                'n_host_id': sub.client_id.host_id.pk,
            })

        postback = PostbackEvent(**postback_data)
        self.session.add(postback)
        await self.session.commit()

    async def check_kass(self, transaction, client):
        if not client:
            return 0

        t_id = transaction.n_terminal_id
        label = ''

        try:
            offer = await self.session.query(Offer).filter_by(id=client.n_offer_id).first()
            if offer:
                label = offer.label
        except:
            pass

        try:
            terminal = await self.session.query(Terminal).filter_by(id=t_id).first()
            if terminal and terminal.kassa_id:
                check = Check(
                    client_id=client,
                    type='Income',
                    n_terminal_id=terminal.id,
                    invoice_id=transaction.invoice_id,
                    label_type='SUBSCRIPTION',
                    price=transaction.amount,
                    quantity=1,
                    amount=transaction.amount,
                    measurement='шт',
                    label=label,
                    create_date_hour=datetime.now().hour
                )
                self.session.add(check)
                await self.session.commit()
        except:
            pass
