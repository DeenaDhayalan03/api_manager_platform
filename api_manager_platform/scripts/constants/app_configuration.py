from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    PROJECT_NAME: str
    ENVIRONMENT: str
    DEBUG: bool
    HOST: str
    PORT: int

    MONGO_URI: str
    MONGO_DB_NAME: str

    USERS_COLLECTION: str
    PLANS_COLLECTION: str
    SERVICES_COLLECTION: str
    SUBSCRIPTIONS_COLLECTION: str
    USAGE_LOGS_COLLECTION: str
    USAGE_SUMMARY_COLLECTION: str
    INVOICES_COLLECTION: str
    ENDPOINT_CREDITS_COLLECTION: str
    NOTIFICATIONS_COLLECTION: str
    SCHEDULED_SUMMARY_COLLECTION: str

    REDIS_URL: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_SOFT_TIME_LIMIT: int
    CELERY_TASK_TIME_LIMIT: int
    CELERY_WORKER_PREFETCH_MULTIPLIER: int
    CELERY_WORKER_CONCURRENCY: int
    CELERY_WORKER_AUTOSCALE: str
    CELERY_BEAT_MONGODB_URI: str

    MQTT_BROKER_URL: str
    MQTT_PORT: int
    MQTT_USERNAME: str
    MQTT_PASSWORD: str
    MQTT_CLIENT_ID: str
    MQTT_KEEPALIVE: int
    MQTT_CLEAN_SESSION: bool
    MQTT_USE_TLS: bool

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    ADMIN_SETUP_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = AppConfig()
