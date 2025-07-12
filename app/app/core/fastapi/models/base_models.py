from typing import Optional
from pytz import timezone as tz
from datetime import datetime as dt
from pydantic import BaseModel, Field, conlist

class NoteSchema(BaseModel):
    """
    Schema for representing a note, including validation for its fields.

    Attributes:
    -----------
    title : str
        The title of the note, with a minimum length of 3 characters and a maximum length of 50 characters.
    
    description : str
        A brief description of the note, with a minimum length of 3 characters and a maximum length of 50 characters.
    
    completed : str
        A flag indicating whether the note is completed. Defaults to "False".
    
    created_date : str
        The date and time when the note was created, formatted as a string in "YYYY-MM-DD HH:MM" format.
        Defaults to the current date and time in the "Europe/Athens" timezone.

    # abstract_json_payload : Optional[Dict]
    #     Optional field for a JSON payload representing additional data for the note. (Currently commented out)
    """
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    completed: str = "False"
    created_date: str = dt.now(tz("Europe/Athens")).strftime("%Y-%m-%d %H:%M")

class NoteDB(NoteSchema):
    """
    Database representation of a note, extending the NoteSchema with an additional identifier.

    Attributes:
    -----------
    id : int
        The unique identifier for the note in the database.
    
    Other attributes are inherited from NoteSchema, including title, description, completed, and created_date.
    """
    id: int 

class SampleResponse(BaseModel):
    """
    Model representing a generic response status.

    Attributes:
    -----------
    status : str
        The status message of the response, typically indicating success or failure.
    """
    status: str

class HealthResponse(BaseModel):
    """
    Model representing a health check response for a service.

    Attributes:
    -----------
    status : str
        The status message of the health check, typically indicating "healthy" or "unhealthy".
    """
    status: str