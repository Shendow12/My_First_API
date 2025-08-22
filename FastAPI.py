from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Job(BaseModel):
    name: str
    description: str
    slary: float
    type: str

class UpdateJob(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slary: Optional[float] = None
    type: Optional[str] = None

class CustomerIDGenerator:
    def __init__(self, start=0):
        self.counter = start

    def generate_customer_id(self):
        self.counter += 1
        return f"{self.counter}"

id_generator = CustomerIDGenerator(start=0)
   
inventory = {}

@app.get("/get-job/{job_id}")
def get_job(job_id: str = Path(..., description="The ID of the job you would like to view")):
    if job_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job ID not found")
    return inventory[job_id]

@app.get("/get-by-name")
def get_job_by_name(name: str = Query(None, title="Name", description="Name of job")):
    for job_id in inventory:
        if inventory[job_id].name == name:
            return inventory[job_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")

@app.post("/create-job")
def create_job(job: Job):
   
    job_id = id_generator.generate_customer_id()
    
    inventory[job_id] = job
    return {"id": job_id, "job": inventory[job_id]}

@app.put("/update-job/{job_id}")
def update_job(job_id: str, job: UpdateJob):
    if job_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job ID does not exist")

    if job.name is not None:
        inventory[job_id].name = job.name

    if job.description is not None:
        inventory[job_id].description = job.description

    if job.slary is not None:
        inventory[job_id].slary = job.slary

    if job.type is not None:
        inventory[job_id].type = job.type

    return inventory[job_id]

@app.delete("/delete-job")
def delete_job(job_id: str = Query(..., description="The ID of the job to delete")):
    if job_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job ID does not exist")

    del inventory[job_id]
    return {"Success": "Job deleted"}