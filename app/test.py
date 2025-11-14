# test_db.py
from db.database import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connexion réussie à la base MySQL ! Résultat :", result.scalar())
    except Exception as e:
        print("❌ Erreur de connexion :", e)

if __name__ == "__main__":
    test_connection()
