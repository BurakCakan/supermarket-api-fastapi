import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy import Table, Column, Integer, String, MetaData

#please complete </> parts below like your postgres credentials
engine = sqlalchemy.create_engine("postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@<POSTGRES_HOST_IP>:5432/<POSTGRES_SCHEMA>")
metadata = MetaData()


team = Table(
    "teams",
    metadata,
    Column("team_id", Integer, primary_key=True),
    Column("name", String),
    Column("endpoint", String),
    Column("api_key", String),
)


def insert_team(name: str, endpoint: str, api_key: str):
    conn = engine.connect()
    try:
        conn.execute(
            team.insert(),
            {"name": name, "endpoint": endpoint, "api_key": api_key},
        )
        conn.commit()
    finally:
        conn.close()


def delete_team(name: str):
    conn = engine.connect()
    try:
        conn.execute(team.delete().where(team.c.name == name))
        conn.commit()
    finally:
        conn.close()


def delete_team_member(id: int):
    conn = engine.connect()
    try:
        result = conn.execute(team.delete().where(team.c.team_id == id))
        conn.commit()
        return result.rowcount > 0
    finally:
        conn.close()

def get_products():
    conn = engine.connect()
    try:
        response = {}
        result = conn.execute(
            text(
                '''
        select 
                pc.name as category_name, 
                p.name 	as product_name, 
                p.product_id as product_id, 
                p.sell_by
        from product p 
        inner join product_category pc on p.product_category_id = pc.product_category_id
        order by category_name desc
        '''))

        for row in result:

            if row[0] not in response.keys():
                product = {}
                product[row[1]] = {'id': row[2], 'sell_by': row[3]}
                response[row[0]] = product
            else:
                product = {}
                product[row[1]] = {'id': row[2], 'sell_by': row[3]}
                response[row[0]][row[1]] = product[row[1]]

        return response

    finally:
        conn.close()
