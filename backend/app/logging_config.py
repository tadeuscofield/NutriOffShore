"""Structured JSON logging configuration for NutriOffshore AI"""
import logging
import json
import sys
import traceback
from datetime import datetime, timezone
from typing import Any


class JSONFormatter(logging.Formatter):
    """Formats log records as JSON for structured log aggregation"""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        # Include extra fields (request_id, path, method, etc.)
        for key in ("request_id", "method", "path", "status_code", "duration_ms",
                     "client_ip", "colaborador_id", "tool_name", "error_detail"):
            value = getattr(record, key, None)
            if value is not None:
                log_entry[key] = value

        return json.dumps(log_entry, default=str, ensure_ascii=False)


def setup_logging(debug: bool = False) -> None:
    """Configure structured JSON logging for the application"""
    level = logging.DEBUG if debug else logging.INFO

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # JSON handler for stdout
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(json_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
