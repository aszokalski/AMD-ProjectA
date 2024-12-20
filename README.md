# Project A
Detailed description of the project and our approach is available in the report file [report.pdf](report.pdf).

Here you can find the instructions to setup, run and use the solution.

## Project Structure
- `assignment` - Contains the assignment files
- `medknow` - Source for the medknow container
- `softknow` - Source for the softknow container
- `report.pdf` - Project report
- `README.md` - This file
- `compose.yml` - Docker compose file
- `Makefile` - Makefile to run the project

## Prerequisites
- Docker
- Docker Compose
- Make
- Python 3.12
- jq (`apt-get install jq`) - for displaying test results

## Setup
1. Clone the repository
2. Run `make` to see the available commands
3. eg. Run `make up` to start the containers

## Data
By default the database will be filled with test data from `medknow/database/POPULATE_DATABASE.sql` which is based on the data from the assignment.

## APIs and Services
- Medknow API docs: http://localhost:2000/docs
- Softknow API docs: http://localhost:3000/docs
- MlFlow: http://localhost:5001

> Run `make medknow` to open MedKnow API docs
> 
> Run `make softknow` to open MedKnow API docs

## Usage
### Medknow API
Is used to register appointments, patients and measurements. Read the API docs to test the endpoints.

Also contains the `/generate_dataset` endpoint to generate a dataset for the SoftKnow Service.

### Softknow
The SoftKnow service is used to help with the diagnosis of patients. It uses the dataset generated by the Medknow API to train a model and exposes two endpoints:
- `/predict` - To predict the diagnosis of a patient
- `/train` - To retrain the model - it fetches the dataset from the Medknow API and trains the model on updated data.

### Example usage
We prepared a test routine to demonstrate the usage of the services.
Run `make test` or `test.http` (in InteliJ) to see the results.

#### Update for Project A1:
We created a new test routine that trains the model for FungiData and opens MLFlow in the browser.

1. Run `make test-a1`
2. Then you need to navigate to
`fungidata.OneR > latest run > Artifacts > oneR_OUTPUT.txt`


The routine will:
1. Call `/train`
2. Call `/predict` with a patient data from `input.json`. Feel free to modify the data to test different scenarios.
