from pydantic import BaseModel, Field


class ChargerSessionModel(BaseModel):
    """Model of a charger session."""
    id: int = Field(alias="session_id")
    energy_kwh: int = Field(alias="energy_delivered_in_kWh")
    duration_sec: int = Field(alias="duration_in_seconds")
    cost_cent: int = Field(alias="session_cost_in_cents")

    class Config:
        # Aliased field can also be populated by its attribute.
        allow_population_by_field_name = True
