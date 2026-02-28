from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    model: str = Field(default="gemini/gemini-1.5-flash")
    api_key: str | None = Field(default=None)
    api_base: str | None = Field(default=None)
    max_tokens: int = Field(default=8192)

default_config = AgentConfig()

metadata = BaseModel()
metadata.name = "Lusaka Website Scout"
metadata.version = "0.1.0"
metadata.description = "Finds and audits poorly designed business websites in Lusaka, Zambia."
