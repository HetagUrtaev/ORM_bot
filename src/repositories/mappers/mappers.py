from src.models import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.users import UserResponse


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserResponse

