from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    애플리케이션 환경 설정을 관리하는 클래스입니다.
    .env 파일의 환경 변수를 읽어옵니다.
    """

    # 프로젝트의 비밀 키
    SECRET_KEY: str

    # JWT 토큰에 사용될 알고리즘
    ALGORITHM: str = "HS256"

    # PostgreSQL 데이터베이스 연결 URL
    SQLALCHEMY_DATABASE_URL: str

    # MongoDB 연결 URL
    MONGO_DATABASE_URL: str

    # MongoDB 데이터베이스 이름
    MONGO_DB_NAME: str

    # Pydantic v2에서 .env 파일을 로드하는 새로운 방식
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Settings 클래스의 인스턴스를 생성하여 전역적으로 사용
settings = Settings()
