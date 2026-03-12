"""
GraphQL フェデレーション（Apollo Federation 互換）
補強スキル: GraphQL フェデレーション
pip install strawberry-graphql[federation]
"""
try:
    import strawberry
    from strawberry.federation import Schema as FederationSchema

    @strawberry.federation.type(keys=["id"])
    class User:
        id: strawberry.ID
        username: str
        email: str

    @strawberry.federation.type(keys=["id"])
    class Project:
        id: strawberry.ID
        name: str
        owner_id: strawberry.ID

    @strawberry.type
    class FederationQuery:
        @strawberry.field
        def _service(self) -> str:
            return "UEP GraphQL Subgraph"

        @strawberry.field
        def user(self, id: strawberry.ID) -> User:
            return User(id=id, username="federated", email="federated@uep.local")

        @strawberry.field
        def project(self, id: strawberry.ID) -> Project:
            return Project(id=id, name="Federated Project", owner_id="u1")

    federation_schema = FederationSchema(query=FederationQuery)
except ImportError:
    federation_schema = None
