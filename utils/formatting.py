def pct(value):
    try:
        return f"{float(value)*100:.1f}%"
    except Exception:
        return "-"
