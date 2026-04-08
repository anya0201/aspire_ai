"""Application configuration via environment variables."""

import os
from pathlib import Path
import secrets

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "development"

    # Database
    database_url: str = ""
    redis_url: str = "redis://localhost:6379/0"

    # LLM — primary provider selection
    llm_provider: str = "gemini"  
    llm_model: str = "gemini-1.5-flash"

    # Cloud providers
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    deepseek_api_key: str = ""
    openrouter_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""

    # Local inference backends
    ollama_base_url: str = "http://localhost:11434"
    vllm_base_url: str = "http://localhost:8000/v1"
    lmstudio_base_url: str = "http://localhost:1234/v1"
    textgenwebui_base_url: str = "http://localhost:5000/v1"

    # Generic OpenAI-compatible endpoint
    custom_llm_api_key: str = ""
    custom_llm_base_url: str = ""
    custom_llm_model: str = ""

    # LiteLLM integration
    use_litellm: bool = False
    litellm_model: str = ""
    litellm_api_base: str = ""
    litellm_api_key: str = ""

    # Model size routing
    llm_model_large: str = ""
    llm_model_small: str = ""
    llm_required: bool = False

    # 3-tier model routing
    llm_model_fast: str = ""
    llm_model_standard: str = ""
    llm_model_frontier: str = ""

    # Authentication
    auth_enabled: bool = True
    deployment_mode: str = "multi_user"
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # CORS
    cors_origins: str = "http://localhost:3001,http://127.0.0.1:3001"

    # File Upload
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 50
    scrape_fixture_dir: str = ""

    # Embedding
    embedding_mode: str = "auto"

    # Runtime bootstrap
    app_auto_create_tables: bool = True
    app_auto_seed_system: bool = True
    app_run_scheduler: bool = False
    app_run_activity_engine: bool = False
    ambient_monitor_enabled: bool = True
    enable_experimental_loom: bool = False
    enable_experimental_lector: bool = False
    enable_experimental_notion_export: bool = False
    enable_experimental_cat: bool = False
    enable_experimental_browser: bool = False
    enable_experimental_vision: bool = False
    voice_enabled: bool = False

    # Rate limiting
    rate_limit_mode: str = "simple"
    rate_limit_rpm: int = 120
    rate_limit_llm_rpm: int = 20
    rate_limit_cost_budget: int = 500
    trust_proxy_headers: bool = False

    # SSE streaming
    sse_timeout_seconds: int = 300

    # Parallel execution
    parallel_context_loading: bool = True
    activity_engine_max_concurrency: int = 3
    activity_use_redis_notify: bool = False

    # Web search
    tavily_api_key: str = ""

    # Workspace
    workspace_max_size_mb: int = 500

    # Code sandbox
    code_sandbox_backend: str = "auto"
    code_sandbox_runtime: str = "docker"
    code_sandbox_timeout_seconds: int = 5
    allow_insecure_process_sandbox: bool = False

    # Encryption
    encryption_key: str = ""

    # Cognitive load signal weights
    cognitive_load_weight_fatigue: float = 0.16
    cognitive_load_weight_session_length: float = 0.08
    cognitive_load_weight_errors: float = 0.14
    cognitive_load_weight_brevity: float = 0.04
    cognitive_load_weight_help_seeking: float = 0.10
    cognitive_load_weight_quiz_performance: float = 0.10
    cognitive_load_weight_answer_hesitation: float = 0.06
    cognitive_load_weight_nlp_affect: float = 0.10
    cognitive_load_weight_relative_baseline: float = 0.08
    cognitive_load_weight_wrong_streak: float = 0.05
    cognitive_load_weight_message_gap: float = 0.05
    cognitive_load_weight_repeated_errors: float = 0.04
    cognitive_load_threshold_high: float = 0.6
    cognitive_load_threshold_medium: float = 0.3

    # Cognitive load normalization constants
    cognitive_load_session_messages_norm: float = 40.0
    cognitive_load_error_count_norm: float = 5.0
    cognitive_load_brevity_length_norm: float = 100.0
    cognitive_load_quiz_accuracy_target: float = 0.7
    cognitive_load_hesitation_min_ms: float = 15000.0
    cognitive_load_hesitation_range_ms: float = 45000.0
    cognitive_load_nlp_frustration_weight: float = 0.6
    cognitive_load_nlp_confusion_weight: float = 0.4
    cognitive_load_review_reorder_threshold: float = 0.5

    # LECTOR review priority factors
    lector_factor_low_mastery: float = 0.5
    lector_factor_never_practiced: float = 0.3
    lector_factor_time_decay: float = 0.3
    lector_factor_prerequisite: float = 0.2
    lector_factor_confusion: float = 0.1
    lector_mastery_threshold: float = 0.8
    lector_prerequisite_threshold: float = 0.5
    lector_confusion_threshold: float = 0.6
    lector_factor_interference: float = 0.15

    # LOOM knowledge graph parameters
    loom_fusion_similarity_threshold: float = 0.85
    loom_interference_similarity_threshold: float = 0.6
    loom_interference_top_n: int = 20
    loom_consolidation_threshold: float = 0.85
    loom_consolidation_parent_boost: float = 0.1
    loom_consolidation_stability_multiplier: float = 1.5

    # BKT mastery parameters
    bkt_default_p_learn: float = 0.10
    bkt_default_slip: float = 0.10

    # FIRe bidirectional propagation
    fire_doubt_per_depth: float = 0.03

    # Logging
    log_file: str = ""
    log_max_bytes: int = 10_485_760
    log_backup_count: int = 5

    @staticmethod
    def _split_csv(value: str) -> list[str]:
        return [item.strip() for item in value.split(",") if item.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return self._split_csv(self.cors_origins)

    @model_validator(mode="after")
    def _resolve_database_url(self):
        """Handle SQLite and Postgres database URLs."""
        if not self.database_url:
            data_dir = Path.home() / ".aspire"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.database_url = f"sqlite+aiosqlite:///{data_dir / 'data.db'}"
            return self

        # Convert Railway's postgres URL to SQLAlchemy async format
        if self.database_url.startswith("postgres://"):
            self.database_url = self.database_url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif self.database_url.startswith("postgresql://"):
            if "+asyncpg" not in self.database_url:
                self.database_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        elif self.database_url.startswith("sqlite"):
            for prefix in ("sqlite+aiosqlite:///", "sqlite:///"):
                if self.database_url.startswith(prefix):
                    sqlite_path = self.database_url[len(prefix):]
                    if sqlite_path.startswith("~"):
                        self.database_url = f"{prefix}{Path(sqlite_path).expanduser()}"
                    break
        return self

    @model_validator(mode="after")
    def _validate_security(self):
        """Simplified security validation for cloud deployment."""
        if not self.jwt_secret_key:
            self.jwt_secret_key = secrets.token_hex(32)
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
