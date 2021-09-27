import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphql_api.api import Query,Mutation


class QueryForSchema(Query, ObjectType):
    pass


schema = graphene.Schema(query=QueryForSchema, mutation=Mutation)
