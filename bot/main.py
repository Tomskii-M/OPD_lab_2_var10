import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
from routers import router as main_router

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Диспетчер
dp = Dispatcher()
dp.include_router(main_router)


# Запуск процесса поллинга новых апдейтов
async def main():
    # Объект бота
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
