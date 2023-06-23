from model.charger_session import ChargerSessionModel


def generate_content():
    topic = "charger/1/connector/1/session/1"
    model = ChargerSessionModel(id=1, energy_kwh=30, duration_sec=45, cost_cent=70)
    return (topic, model.json(by_alias=True))
