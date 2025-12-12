"""
Configuration loader for NL2SQL system.
M0: Basic configuration without LLM providers.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any


# Load .env file
load_dotenv()


class Config:
    """Configuration manager for NL2SQL system."""

    def __init__(self):
        """Initialize basic M0 configuration."""
        self._load_env_vars()

    def _load_env_vars(self):
        """Load environment variables."""
        # Basic configuration for M0
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return getattr(self, key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "debug": self.debug
        }


def load_config() -> Config:
    """Load configuration instance."""
    return Config()


def test_config():
    """Test configuration loading."""
    print("=== NL2SQL 配置测试 ===\n")
    
    config = load_config()
    
    print("基础配置:")
    print(f"  调试模式: {config.debug}")
    print("  ✓ 配置加载成功")


if __name__ == "__main__":
    test_config()