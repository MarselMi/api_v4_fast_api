from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from sqlalchemy import ForeignKey, UniqueConstraint


class PartnerOfTheManagerAssociation(Base):
    __tablename__ = "partners_of_the_manager_association"

    partner_id: Mapped[int] = mapped_column(
        ForeignKey("partners.id", ondelete="CASCADE"),
    )
    manager_id: Mapped[int] = mapped_column(
        ForeignKey("managers.id", ondelete="CASCADE"),
    )


class PartnerOfThePrivateOffersAssociation(Base):
    __tablename__ = "partners_of_the_offer_association"

    partner_id: Mapped[int] = mapped_column(
        ForeignKey("partners.id", ondelete="CASCADE"),
    )
    offer_id: Mapped[int] = mapped_column(
        ForeignKey("offers.id", ondelete="CASCADE"),
    )


class PartnerOfThePrivateLandingsAssociation(Base):
    __tablename__ = "partners_of_the_landings_association"

    partner_id: Mapped[int] = mapped_column(
        ForeignKey("partners.id", ondelete="CASCADE"),
    )
    landing_id: Mapped[int] = mapped_column(
        ForeignKey("landings.id", ondelete="CASCADE"),
    )


class PartnerOfThePrivatePrelandingsAssociation(Base):
    __tablename__ = "partners_of_the_prelandings_association"

    partner_id: Mapped[int] = mapped_column(
        ForeignKey("partners.id", ondelete="CASCADE"),
    )
    prelanding_id: Mapped[int] = mapped_column(
        ForeignKey("prelandings.id", ondelete="CASCADE"),
    )


class HostOfThePostbackAssociation(Base):
    __tablename__ = "host_of_the_postback_association"

    host_id: Mapped[int] = mapped_column(
        ForeignKey("hosts.id", ondelete="CASCADE"),
    )
    postback_id: Mapped[int] = mapped_column(
        ForeignKey("postbacks.id", ondelete="CASCADE"),
    )


class LandingOfThePartnerAssociation(Base):
    __tablename__ = "landing_of_the_partner_association"

    partner_id: Mapped[int] = mapped_column(
        ForeignKey("partners.id", ondelete="CASCADE"),
    )
    landing_id: Mapped[int] = mapped_column(
        ForeignKey("landings.id", ondelete="CASCADE"),
    )


class EventsOfThePostbackAssociation(Base):
    __tablename__ = "events_of_the_postback_association"

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"),
    )
    postback_id: Mapped[int] = mapped_column(
        ForeignKey("postbacks.id", ondelete="CASCADE"),
    )


class StreamsOfThePostbackAssociation(Base):
    __tablename__ = "streams_of_the_postback_association"

    stream_id: Mapped[int] = mapped_column(
        ForeignKey("streams.id", ondelete="CASCADE"),
    )
    postback_id: Mapped[int] = mapped_column(
        ForeignKey("postbacks.id", ondelete="CASCADE"),
    )
