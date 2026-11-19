from datetime import datetime, timedelta

from src.schemas.users import UserResponse


async def test_upsert_users(db):
    test_tg_id = 999_888_777
    first_time = datetime(2026, 11, 14, 12, 0, 0)
    second_time = first_time + timedelta(minutes=15)

    first_user_data = UserResponse(
        telegram_id=test_tg_id,
        first_name="Тест",
        last_name="Юзер",
        username="test_db_user",
        language_code="ru",
        is_premium=False,
        is_bot=False,
        created_at=first_time,
        last_activity_at=first_time,
    )

    await db.users.upsert(first_user_data)
    await db.commit()

    saved_user = await db.users.get_one_or_none(telegram_id=test_tg_id)
    assert saved_user is not None
    assert saved_user.created_at == first_time
    assert saved_user.last_activity_at == first_time

    updated_data = first_user_data.model_copy(
        update={"created_at": second_time, "last_activity_at": second_time}
    )
    await db.users.upsert(updated_data)
    await db.commit()

    user_after_update = await db.users.get_one_or_none(telegram_id=test_tg_id)
    assert user_after_update is not None
    assert user_after_update.created_at == first_time
    assert user_after_update.last_activity_at == second_time