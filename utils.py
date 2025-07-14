async def find_user(bot, username: str) -> tuple | None:
    try:
        response = await bot.highrise.get_room_users()
        return next(((u, pos) for u, pos in response.content
                     if u.username.lower() == username.lower()), None)
    except Exception as e:
        print(f"Error in find_user: {e}")
        return None
