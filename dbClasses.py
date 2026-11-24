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

    users_id: int | None = Field(default=None, foreign_key="users.id")
    plan_id: int | None = Field(default=None, foreign_key="subscriptionplans.id")

# session bookings
class Sessions(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    time: datetime

    trainer_id: int | None = Field(default=None, foreign_key="users.id")

class Booking(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="users.id")
    session_id: int | None = Field(default=None, foreign_key="sessions.id")

# posts
class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    url: str
    last_change: datetime
    date_published: datetime
    paid: bool

    author_id: int | None = Field(default=None, foreign_key="users.id")

class Tags(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    catagory: str

class PostTags(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    post_id: int | None = Field(default=None, foreign_key="posts.id")
    tag_id: int | None = Field(default=None, foreign_key="tags.id")

# trackers
class Trackers(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="users.id")
    trainer_id: int | None = Field(default=None, foreign_key="users.id")

class Exercises(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    count_mesurement: str
    deafult_count: int

class TrackerExercises(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    tracker_id: int | None = Field(default=None, foreign_key="trackers.id")
    exercise_id: int | None = Field(default=None, foreign_key="exercises.id")

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
