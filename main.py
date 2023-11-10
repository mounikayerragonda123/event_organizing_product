from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI ,APIRouter,Depends,HTTPException
from sqlalchemy.exc import SQLAlchemyError
import models
from models import users , event , approval
from request import userrequest,eventrequest,approverequest
import models
from database import engine, SessionLocal
from starlette import status
import logging


app=FastAPI()


"""try:
    models.Base.metadata.create_all(bind=engine)
    print("Tables created successfully")
except SQLAlchemyError as e:
    print(f"Error creating tables: {str(e)}")"""

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.INFO,  # Set the desired log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="eventproduct.log",  # Specify the log file name and location
    filemode="w",  # Use 'w' for overwrite, or 'a' for append
)


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session, Depends(get_db)]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.get("/")
async def read_users(db:db_dependency):
    try:
        user=db.query(users).all()
        logger.info("Read user details successfully")
        return user
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,user_request: userrequest):
    try:
        create_model=users(**user_request.dict())
        db.add(create_model)
        db.commit()
        db.refresh(create_model)
        logger.info("created user details successfully")
        return create_model
    except Exception as e:
        db.rollback()
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')


@app.put("/user/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db:db_dependency,
                      user_id:int,user_request: userrequest):
    try:
        user_model=db.query(users).filter(users.user_id==user_id).first()
        if user_model is None:
            raise HTTPException(status_code=404, detail='user not found')

        user_model.user_name=user_request.user_name
        user_model.user_email = user_request.user_email
        user_model.contact_no = user_request.contact_no
        user_model.address = user_request.address
        user_model.password = user_request.password
        user_model.user_role = user_request.user_role
        user_model.created_by = user_request.created_by
        user_model.updated_by = user_request.updated_by

        db.add(user_model)
        db.commit()
        logger.info(f"Updated user details for user_id {user_id} successfully")

    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an exception
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')

@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(db:db_dependency,
                      user_id:int):
    try:
        user_model = db.query(users).filter(users.user_id == user_id).first()
        if user_model is None:
            raise HTTPException(status_code=404, detail='user not found')
        db.query(users).filter(users.user_id==user_id).delete()
        db.commit()
        logger.info(f"Deleted user details for user_id {user_id} successfully")
    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an exception
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')

@app.get("/events_details")
async def read_events(db: db_dependency):
    try:
        events=db.query(event).all()
        logger.info("Read event details successfully")
        return events

    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')



@app.get("/organizer_details/",status_code=status.HTTP_200_OK)
async def read_events(db: db_dependency,organizer_id: int):
    try:
        event_model= db.query(event).filter(event.organizer_id==organizer_id)\
            .filter(event.organizer_id==users.user_id).first()
        if event_model is not None:
            logger.info(f"Retrieved organizer details for organizer_id {organizer_id} successfully")
            return event_model
        raise HTTPException(status_code=404,detail='ticket model is not found')
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')

@app.post("/create_event_details/")
async def create_events(db:db_dependency,event_request: eventrequest):
    try:
        event_model = event(**event_request.dict())
        db.add(event_model)
        db.commit()
        logger.info("Created event details successfully")

    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an exception
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')


@app.put("/update_event_details/{event_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_event(db:db_dependency,event_request: eventrequest,
                         ticket_id: int):
    try:
        event_model=db.query(event).filter(event.ticket_id==ticket_id).first()
        event_model = event(**event_request.dict())
        db.add(event_model)
        db.commit()
        logger.info(f"Updated event details for user_id {ticket_id} successfully")
    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an exception
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')


@app.delete("/events/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_events(db:db_dependency,
                      ticket_id:int):
    try:
        event_model = db.query(event).filter(event.ticket_id == ticket_id).first()
        if event_model is None:
            raise HTTPException(status_code=404, detail='ticket not found')
        db.query(event).filter(event.ticket_id == ticket_id).delete()
        db.commit()
        logger.info(f"Deleted event details for user_id {ticket_id} successfully")
    except Exception as e:
        # Handle any exceptions that may occur during the delete process
        db.rollback()
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@app.get("/Approval_details")
async def read_approval_info(db: db_dependency):
    try:
        approve=db.query(approval).all()
        logger.info("Retreive approval details successfully")
        return approve
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')


@app.post("/create_approval_data", status_code=status.HTTP_201_CREATED)
async def create_approval_data(db:db_dependency,approve_request: approverequest):
    try:
        approve_model=approval(**approve_request.dict())
        db.add(approve_model)
        db.commit()
        logger.info("Created approval details successfully")
    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an exception
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')

@app.put("/upadate_approval_info",status_code=status.HTTP_204_NO_CONTENT)
async def update_approval_info(db:db_dependency,
                      approval_id:int,approve_request: approverequest):
    try:
        approve_model=db.query(approval).filter(approval.approval_id==approval_id).first()
        if approve_model is None:
            raise HTTPException(status_code=404, detail='approval not found')
        db.add(approve_model)
        db.commit()
        logger.info(f"Updated event details for user_id {approval_id} successfully")

    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an exception
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {str(e)}')


@app.delete("del_approval_details", status_code=status.HTTP_204_NO_CONTENT)
async def delete_approval_details(db:db_dependency,
                      approval_id:int):
    try:
        approve_model = db.query(approval).filter(approval.approval_id==approval_id).first()
        if approve_model is None:
            raise HTTPException(status_code=404, detail='approval details not found')
        db.query(users).filter(approval.approval_id==approval_id).delete()
        db.commit()
        logger.info(f"Deleted event details for user_id {approval_id} successfully")
    except Exception as e:
        # Handle any exceptions that may occur during the delete process
        db.rollback()
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")







