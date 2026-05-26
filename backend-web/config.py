import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """
    Central configuration class that reads from environment variables.
    All sensitive values should be set in .env (see .env.example).
    """

    # ── App ──────────────────────────────────────────────────────────────
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")

    # ── Xianyu / Taobao credentials ──────────────────────────────────────
    XIANYU_COOKIE: str = os.getenv("XIANYU_COOKIE", "")
    XIANYU_USER_ID: str = os.getenv("XIANYU_USER_ID", "")

    # ── AI / LLM backend ─────────────────────────────────────────────────
    AI_BASE_URL: str = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    # System prompt injected into every conversation
    AI_SYSTEM_PROMPT: str = os.getenv(
        "AI_SYSTEM_PROMPT",
        "You are a helpful Xianyu (闲鱼) seller assistant. "
        "Reply politely and concisely in Chinese.",
    )

    # ── WebSocket heartbeat ───────────────────────────────────────────────
    WS_HEARTBEAT_INTERVAL: int = int(os.getenv("WS_HEARTBEAT_INTERVAL", 30))
    WS_RECONNECT_DELAY: int = int(os.getenv("WS_RECONNECT_DELAY", 5))
    WS_MAX_RECONNECT_ATTEMPTS: int = int(os.getenv("WS_MAX_RECONNECT_ATTEMPTS", 10))

    # ── Database (optional persistence layer) ────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'xianyu.db'}"
    )

    # ── Logging ───────────────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: str = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "app.log"))

    # ── Rate limiting (messages per minute per buyer) ────────────────────
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", 10))

    # ── Auto-reply toggle ─────────────────────────────────────────────────
    AUTO_REPLY_ENABLED: bool = (
        os.getenv("AUTO_REPLY_ENABLED", "true").lower() == "true"
    )

    def validate(self) -> None:
        """
        Raise ValueError for any required but missing configuration values.
        Call this once at application startup.
        """
        missing = []
        if not self.XIANYU_COOKIE:
            missing.append("XIANYU_COOKIE")
        if not self.XIANYU_USER_ID:
            missing.append("XIANYU_USER_ID")
        if not self.AI_API_KEY:
            missing.append("AI_API_KEY")
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Please check your .env file."
            )


# Singleton instance used throughout the application
config = Config()
