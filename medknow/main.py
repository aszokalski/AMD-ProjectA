from fastapi import FastAPI, Request
from logging import getLogger
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool


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

    return ({"data": dataset})
