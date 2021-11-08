import datetime


async def get_meal_type():
    today = datetime.datetime.now()
    hour = today.hour
    minute = today.minute

    if hour < 8 or hour == 8 and minute <= 10:
        meal_type = "breakfast"
    elif hour < 13 or hour == 13 and minute <= 10:
        meal_type = "lunch"
    elif hour < 18 or hour == 18 and minute <= 50:
        meal_type = "dinner"
    else:
        meal_type = "nextBreakfast"
    return meal_type
