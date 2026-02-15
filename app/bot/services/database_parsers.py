def joined_row_parser(row):
    user, alarm = row
    return {
        'chat_id': user.chat_id,
        'timezone': getattr(user, 'timezone', None),
        'language': getattr(user, 'language', None),
        'alarm_id': alarm.alarm_id,
        'is_repeated': alarm.is_repeated,
        'datetime': alarm.datetime,
        'cron': alarm.cron,
    }
