from app.infrastructure.data_classes.data_classes import AlarmJoinedOnUser, UserSettings
from app.bot.services.cron_parsers import parse_cron_from_string

def joined_row_parser(row) -> AlarmJoinedOnUser:
    user, alarm = row
    if alarm.cron is not None:
        cron = parse_cron_from_string(alarm.cron)
    else:
        cron = None
    alarm_joined_on_user = AlarmJoinedOnUser(
        alarm_id=alarm.alarm_id,
        chat_id=alarm.chat_id,
        user_settings=UserSettings(
            timezone=user.timezone,
            language=user.language,
        ),
        is_repeated=alarm.is_repeated,
        datetime=alarm.datetime,
        cron=cron,
    )
    return alarm_joined_on_user
