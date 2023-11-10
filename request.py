from pydantic import BaseModel
from datetime import datetime

class userrequest(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    password:str
    contact_no: int
    address: str
    user_role:str
    created_by:str
    created_at:datetime
    updated_by:str
    updated_at:datetime


class eventrequest(BaseModel):

    event_id:int
    ticket_id:int
    event_name:str
    event_description:str
    organizer_id:int
    organizer_details:str
    event_date:datetime
    venue_name:str
    venue_address:str
    venue_capacity:int
    ticket_type : str
    ticket_price :int
    quantity_available :int
    attached_id:int
    attachment_url:str
    attachment_description:str
    timestamp:datetime
    created_by:str
    created_at:datetime
    updated_by:str
    updated_at:datetime

class approverequest(BaseModel):
    approval_id :int
    event_name :str
    description :str
    event_date:datetime
    evnts_id :int
    approver_id :int
    approval_status :str
