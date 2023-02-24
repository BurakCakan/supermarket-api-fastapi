from fastapi import FastAPI, HTTPException
from src.models.grocerytype import groceryType
from src.models.team import Team
from src.database import insert_team, delete_team, get_products, delete_team_member

app = FastAPI()


@app.get("/")
async def dead_root():
    return {"Hello": "World"}

@app.get("/products")
async def list_products():

    try:
        response_model = get_products()
        return response_model
    
    except  HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{type}")
async def list_products(type: groceryType):

    try:
        response_model = get_products()
        return response_model[type]
    
    except  HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/team/")
async def add_team(team: Team):

    try:
        insert_team(team.name, team.endpoint, team.api_key)
        return {"response": f' {team.name} is added to the table'}
    
    except  HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete_team_name/{team_name}")
async def del_team(team_name):

    try:
        delete_team(team_name)
        return {"response": f' {team_name} is deleted from the table!'}
    
    except  HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/team/{record_id}")
async def delete_team_member_by_id(record_id: int):

    try:
        response = delete_team_member(record_id)
        if not response:
            raise HTTPException(status_code=404, detail="The record is not available in the table")

        return {"response": f"Record with ID {record_id} has been deleted from team table."}
    
    except  HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

