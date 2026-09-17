def get_decision_signals(data):
    alerts = data.get("active_alerts", 0)
    klb = float(data.get("klb_signal", 0) or 0)
    if klb >= 0.80 or alerts >= 10:
        priority = "Prioritas tinggi"
    elif klb >= 0.60 or alerts >= 5:
        priority = "Perlu perhatian"
    else:
        priority = "Pemantauan"
    return {"priority": priority, "klb_signal": klb, "active_alerts": alerts}
