from pydantic import BaseModel
from enum import Enum
from datetime import date

class Age(str, Enum):
    YOUNG = "young"
    PRESBYOPIC = "presbyopic"
    PRE_PRESBYOPIC = "pre-presbyopic"

class TearRate(str, Enum):
    NORMAL = "normal"
    REDUCED = "reduced"

class LensType(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    NONE = "none"

class PrescriptionType(str, Enum):
    MYOPE = "myope"
    HYPERMETROPE = "hypermetrope"
    NONE = "none"

class MeasurementCreate(BaseModel):
    measurement_date: date
    expiration_date: date
    age: Age
    tear_rate: TearRate
    astigmatic: bool
    prescription: PrescriptionType
    last_measurement_id: int = None

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    lens_type: LensType
    used_measurement_id: int