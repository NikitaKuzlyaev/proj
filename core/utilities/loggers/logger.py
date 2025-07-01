import logging

# # Полностью отключить SQLAlchemy
# logging.getLogger("sqlalchemy").setLevel(logging.WARNING)           # или ERROR
# logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)    # убирает SQL-запросы
# logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
