from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine

# subscriptions
class SubscriptionPlans(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    frequency: int
    price: float

class Subscriptions(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    payment_provider_id: str
    next_payment: datetime

    plan: int | None = Field(default=None, foreign_key="subscriptionplans.id")

# session bookings
class Session(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    time: datetime

    trainer: int | None = Field(default=None, foreign_key="users.id")

class Booking(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: int | None = Field(default=None, foreign_key="users.id")
    session: int | None = Field(default=None, foreign_key="session.id")

# users
class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    dob: datetime
    password: str
    created: datetime
    active: bool
    member: bool
    accountType: int

    subscription_id : int | None = Field(default=None, foreign_key="subscriptions.id")
