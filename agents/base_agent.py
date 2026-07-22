"""
base_agent.py

The BaseAgent class defines the common lifecycle for every AI agent in
the AI-Agent-Framework.

Every future agent (Collection, Cleaning, Validation, Reporting, etc.)
inherits from this class.

Author: Jacob Idinye
"""

from __future__ import annotations

import logging
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional


# ---------------------------------------------------------
# Agent Status
# ---------------------------------------------------------

class AgentStatus(Enum):
    """Represents the current state of an AI Agent."""

    IDLE = "Idle"
    RUNNING = "Running"
    SUCCESS = "Success"
    FAILED = "Failed"
    STOPPED = "Stopped"


# ---------------------------------------------------------
# Base Agent
# ---------------------------------------------------------

class BaseAgent(ABC):
    """
    Base class for all AI agents.

    Every agent in the framework inherits from this class.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        config: Optional[Dict[str, Any]] = None,
    ):

        self.id = str(uuid.uuid4())

        self.name = name

        self.description = description

        self.status = AgentStatus.IDLE

        self.config = config or {}

        self.created_at = datetime.now()

        self.started_at = None

        self.finished_at = None

        self.metrics = {}

        self.logger = self._create_logger()

    # -----------------------------------------------------

    def _create_logger(self):

        """
        Creates a logger for this agent.
        """

        Path("logs").mkdir(exist_ok=True)

        logger = logging.getLogger(self.name)

        logger.setLevel(logging.INFO)

        if not logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            file_handler = logging.FileHandler(
                f"logs/{self.name}.log"
            )

            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

            logger.addHandler(console_handler)

        return logger

    # -----------------------------------------------------

    def start(self):

        self.started_at = datetime.now()

        self.status = AgentStatus.RUNNING

        self.logger.info(f"{self.name} started.")

    # -----------------------------------------------------

    def stop(self):

        self.finished_at = datetime.now()

        self.status = AgentStatus.STOPPED

        self.logger.info(f"{self.name} stopped.")

    # -----------------------------------------------------

    def success(self):

        self.finished_at = datetime.now()

        self.status = AgentStatus.SUCCESS

        runtime = self.runtime()

        self.logger.info(
            f"{self.name} completed successfully "
            f"in {runtime:.2f} seconds."
        )

    # -----------------------------------------------------

    def fail(self, exception):

        self.finished_at = datetime.now()

        self.status = AgentStatus.FAILED

        self.logger.exception(exception)

    # -----------------------------------------------------

    def runtime(self):

        if self.started_at is None:

            return 0

        end = self.finished_at or datetime.now()

        return (end - self.started_at).total_seconds()

    # -----------------------------------------------------

    def update_metric(self, key, value):

        self.metrics[key] = value

    # -----------------------------------------------------

    def get_metric(self, key):

        return self.metrics.get(key)

    # -----------------------------------------------------

    def health_check(self):

        return {
            "agent": self.name,
            "status": self.status.value,
            "runtime": self.runtime(),
            "metrics": self.metrics,
        }

    # -----------------------------------------------------

    def run(self):

        """
        Main lifecycle.

        Do NOT override this.

        Override execute().
        """

        try:

            self.start()

            result = self.execute()

            self.success()

            return result

        except Exception as e:

            self.fail(e)

            raise

    # -----------------------------------------------------

    @abstractmethod
    def execute(self):

        """
        Child classes implement this.
        """
        pass