from logging.config import fileConfig
from app.database import Base  # Убедитесь, что импортируете правильный Base
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Указываем метаданные для автогенерации миграций
target_metadata = Base.metadata

# Этот объект конфигурации Alembic предоставляет доступ
# к значениям из используемого .ini файла.
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Настройка URL базы данных
config.set_main_option('sqlalchemy.url', 'sqlite:///./dlm_warehouse.db')


def run_migrations_offline() -> None:
    """Запустить миграции в 'offline' режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запустить миграции в 'online' режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
