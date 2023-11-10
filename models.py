from sqlalchemy import Column, DateTime, Time, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    user_name = Column(String)
    user_email = Column(String)
    password = Column(String)
    contact_no = Column(Integer)
    address = Column(String)
    user_role = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime)
    updated_by = Column(String)
    updated_at = Column(DateTime)

class event(Base):
    __tablename__ = 'event'

    event_id = Column(Integer, primary_key=True, index=True, unique=True)
    ticket_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)
    event_description = Column(String)
    organizer_id = Column(Integer, ForeignKey("users.user_id"))
    organizer_details = Column(String)
    event_date = Column(DateTime)
    venue_name = Column(String)
    venue_address = Column(String)
    venue_capacity = Column(Integer)
    ticket_type = Column(String)
    ticket_price = Column(Integer)
    quantity_available = Column(Integer)
    attached_id = Column(Integer, ForeignKey("users.user_id"))
    attachment_url = Column(String)
    attachment_description = Column(String)
    timestamp = Column(DateTime)
    created_by = Column(String)
    created_at = Column(DateTime)
    updated_by = Column(String)
    updated_at = Column(DateTime)

class approval(Base):
    __tablename__ = 'approval'

    approval_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    description = Column(String)
    event_date = Column(DateTime)
    evnts_id = Column(Integer,ForeignKey("event.event_id"))
    approver_id = Column(Integer,ForeignKey("users.user_id"))
    approval_status = Column(String)



"""from database import Base
from sqlalchemy import Column, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetimes

Base = declarative_base()


class users(Base):
    __tablename__='users'

    user_id=Column(Integer,primary_key=True, index=True)
    user_name=Column(String)
    user_email = Column(String)
    password=Column(String)
    contact_no= Column(Integer)
    address=Column(String)
    user_role=Column(String)
    created_by=Column(String)
    created_at=Column(DateTime)
    updated_by=Column(String)
    updated_at=Column(DateTime)


class event(Base):
    __tablename__ = 'event'

    event_id=Column(Integer, primary_key=True)
    ticket_id = Column(Integer, primary_key=True)
    event_name=Column(String)
    event_description=Column(String)
    Organizer_id=Column(Integer,ForeignKey("users.user_id"))
    organizer_details=Column(String)
    Date=Column(String)
    time=Column(String)
    Venue_name=Column(String)
    Venue_address=Column(String)
    Venue_capacity=Column(String)
    ticket_type = Column(String)
    ticket_price = Column(Integer)
    quantity_available =Column(Integer)
    attached_id=Column(Integer,ForeignKey("users.user_id"))
    attachment_url=Column(String)
    attachment_description=Column(String)
    timestamp=Column(String)
    created_by= Column(String)
    created_at= Column(DateTime)
    updated_by= Column(String)
    updated_at= Column(DateTime)

class approval(Base):
    __tablename__ = 'approval'

    approval_id=Column(Integer, primary_key=True)
    event_name=Column(String)
    Description=Column(String)
    Date=Column(String)
    time=Column(String)
    evnts_id = Column(Integer,ForeignKey("event.event_id"))
    approver_id=Column(Integer,ForeignKey("users.user_id"))
    approval_status=Column(String)"""


