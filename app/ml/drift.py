from app.database import engine

def calculate_drift():

    avg_conf = engine.execute("""
        SELECT AVG(confidence)
        FROM expenses
        WHERE confidence IS NOT NULL
    """).fetchone()[0] or 0

    acc = engine.execute("""
        SELECT accuracy
        FROM model_registry
        WHERE is_active = TRUE
    """).fetchone()[0] or 0

    drift = abs(acc - avg_conf)

    engine.execute("""
        INSERT INTO drift_metrics (avg_confidence, drift_score)
        VALUES (%s, %s)
    """, (avg_conf, drift))

    return drift