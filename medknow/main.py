from fastapi import FastAPI, Request, HTTPException, status
from logging import getLogger
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from psycopg import OperationalError
from model import MeasurementCreate, AppointmentCreate

TARGET_COLUMN = "lens_type"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = AsyncConnectionPool(conninfo=get_conn_str())
    yield
    await app.async_pool.close()


app = FastAPI(lifespan=lifespan)
logger = getLogger(__name__)

def get_conn_str():
    return f"""
    dbname = postgres
    user = postgres
    password = postgres
    port = 5432
    host=postgres
    """

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate_dataset")
async def generate_dataset(request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT
                    m.astigmatic,
                    m.age_id,
                    m.tear_rate_id,
                    m.prescription_type_id,
                    a.lens_type_id
                FROM
                    public.measurements m
                JOIN
                    public.appointments a ON m.measurement_id = a.used_measurement_id;
                    """)
            results = await cur.fetchall()
            print(results)
            dataset = []
            for row in results:
                dataset.append({
                    "astigmatic": row[0],
                    "age": row[1],
                    "tear_rate": row[2],
                    "prescription": row[3],
                    "lens_type": row[4],
                })

    return {
        "data": dataset,
        "target": TARGET_COLUMN
    }

async def get_enum_id(request: Request, table: str, name: str) -> int:
    # Define the correct ID column name for each table
    id_column = {
        "ages": "age_id",
        "tear_rates": "tear_rate_id",
        "prescription_types": "prescription_type_id",
        "lens_type": "lens_type_id"
    }.get(table)

    if not id_column:
        raise HTTPException(status_code=500, detail=f"Invalid table name: {table}")

    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT {id_column} FROM public.{table} WHERE name = %s;", (name,))
            result = await cur.fetchone()
            if result:
                return result[0]
            else:
                raise HTTPException(status_code=404, detail=f"{name} not found in {table}")


@app.post("/add_measurement", status_code=status.HTTP_201_CREATED)
async def add_measurement(request: Request, measurement: MeasurementCreate):
    try:
        age_id = await get_enum_id(request, "ages", measurement.age.value)
        tear_rate_id = await get_enum_id(request, "tear_rates", measurement.tear_rate.value)
        prescription_type_id = await get_enum_id(request, "prescription_types", measurement.prescription.value)

        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO public.measurements 
                    (measurement_date, expiration_date, age_id, tear_rate_id, astigmatic, prescription_type_id, last_measurement_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING measurement_id;
                    """, (
                    measurement.measurement_date,
                    measurement.expiration_date,
                    age_id,
                    tear_rate_id,
                    measurement.astigmatic,
                    prescription_type_id,
                    measurement.last_measurement_id
                ))
                measurement_id = (await cur.fetchone())[0]
        logger.info(f"Measurement added with ID {measurement_id}")
        return {"measurement_id": measurement_id, "status": "success"}
    except OperationalError:
        logger.error("Database connection failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Database connection failed")
    except Exception as e:
        logger.error("Failed to add measurement", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to add measurement")

@app.post("/add_appointment", status_code=status.HTTP_201_CREATED)
async def add_appointment(request: Request, appointment: AppointmentCreate):
    try:
        lens_type_id = await get_enum_id(request, "lens_type", appointment.lens_type.value)

        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO public.appointments 
                    (patient_id, doctor_id, appointment_date, lens_type_id, used_measurement_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING patient_id, appointment_date;
                    """, (
                    appointment.patient_id,
                    appointment.doctor_id,
                    appointment.appointment_date,
                    lens_type_id,
                    appointment.used_measurement_id
                ))
                patient_id, appointment_date = await cur.fetchone()
        logger.info(f"Appointment added for patient ID {patient_id} on {appointment_date}")
        return {"patient_id": patient_id, "appointment_date": appointment_date, "status": "success"}
    except OperationalError:
        logger.error("Database connection failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Database connection failed")
    except Exception as e:
        logger.error("Failed to add appointment", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to add appointment")
