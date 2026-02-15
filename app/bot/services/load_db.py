from app.infrastructure.data_classes.data_classes import AlarmJoinedOnUser
from app.infrastructure.database.queries import get_alarms_joined_on_users
from app.bot.services.database_parsers import joined_row_parser


async def load_db() -> list[AlarmJoinedOnUser]:
    db = await get_alarms_joined_on_users()
    alarms_list: list = []
    for row in db:
        alarms_list.append(joined_row_parser(row))
    return alarms_list
