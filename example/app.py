
from fastapi import FastAPI, Request, Depends, APIRouter, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette_graphene3 import GraphQLApp, make_playground_handler
from graphene import ObjectType, String, Schema
from starlette.status import HTTP_403_FORBIDDEN
from example.config import API_KEY, API_KEY_NAME

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    
class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    async def resolve_hello(root, info, name):
        return f'Hello {name}!'

    async def resolve_goodbye(root, info):
        return 'See ya!'

schema = Schema(query=Query)


graphql_app = GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
)


async def wrapper(req: Request) -> None:
    await graphql_app(req.scope, req.receive, req._send)

app = FastAPI()
router = APIRouter(tags=["graphql"])

router.add_api_route(
    "/graphql", wrapper, dependencies=[Depends(get_api_key)], include_in_schema=True, methods=["POST"]
)

router.add_api_route(
    "/graphql", wrapper, include_in_schema=True, methods=["GET"]
)

router.add_api_websocket_route("/graphql", graphql_app)
app.include_router(router)


