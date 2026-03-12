"""Seed initial data - Medical, Aviation, Space（中身を濃く）"""
import sys
import time
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError


def _hash_password(password: str) -> str:
    """passlib に依存せず bcrypt を直接使用（コンテナの passlib/bcrypt 互換問題を回避）"""
    import bcrypt
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Config must see DATABASE_URL_SYNC before database import
def seed(force: bool = False):
    from database import sync_engine, Base
    from models import User, Patient, AIDiagnosis, VitalSign, Flight, Airport, Satellite, Launch, Notification

    for attempt in range(5):
        try:
            Base.metadata.create_all(sync_engine)
            break
        except OperationalError as e:
            if attempt < 4:
                print(f"DB not ready, retry {attempt+1}/5: {e}", file=sys.stderr)
                time.sleep(2)
            else:
                print(f"DB connection failed: {e}", file=sys.stderr)
                sys.exit(1)
    with Session(sync_engine) as s:
        # Users（常にupsert。早期returnの前に行う）
        for u in [
            User(username="kaho0525", password_hash=_hash_password("0525"), role="admin"),
            User(username="admin", password_hash=_hash_password("admin"), role="admin"),
        ]:
            existing = s.execute(select(User).where(User.username == u.username)).scalars().first()
            if existing:
                existing.password_hash = u.password_hash
                existing.role = u.role
            else:
                s.add(u)
        s.commit()

        if not force and s.execute(select(Patient)).scalars().first():
            return
        if force:
            for t in ["notifications", "ai_diagnoses", "vital_signs", "patients", "flights", "airports", "satellites", "launches"]:
                try:
                    s.execute(text(f"TRUNCATE TABLE {t} CASCADE"))
                except Exception:
                    pass
            s.commit()
        # Notifications（通知センター用）
        has_notif = s.execute(select(Notification)).scalars().first()
        if force or not has_notif:
            for n in [
                Notification(title="Medical: AI診断 レビュー待ち", body="2件のAI診断がレビュー待ちです", severity="info", domain="medical"),
                Notification(title="Aviation: 定時率良好", body="本日の定時率 92%", severity="success", domain="aviation"),
                Notification(title="Space: ISS 軌道正常", body="ISS の軌道は正常です", severity="info", domain="space"),
            ]:
                s.add(n)
        s.commit()
        # Medical（中身を濃く）
        patients = [
            Patient(id="P001", identifier="P001", family_name="山田", given_name="太郎", gender="male", birth_date="1980-01-01"),
            Patient(id="P002", identifier="P002", family_name="佐藤", given_name="花子", gender="female", birth_date="1985-05-15"),
            Patient(id="P003", identifier="P003", family_name="鈴木", given_name="一郎", gender="male", birth_date="1972-11-20"),
            Patient(id="P004", identifier="P004", family_name="高橋", given_name="美咲", gender="female", birth_date="1990-03-08"),
            Patient(id="P005", identifier="P005", family_name="伊藤", given_name="健", gender="male", birth_date="1965-07-12"),
        ]
        for p in patients:
            s.add(p)
        s.commit()
        for d in [
            AIDiagnosis(patient_id="P001", finding="Chest X-ray abnormality, follow-up recommended", confidence=0.94, status="Review"),
            AIDiagnosis(patient_id="P002", finding="Normal findings", confidence=0.99, status="Done"),
            AIDiagnosis(patient_id="P003", finding="Cardiac rhythm irregularity detected", confidence=0.87, status="Review"),
            AIDiagnosis(patient_id="P004", finding="Minor opacity in lower lobe", confidence=0.76, status="Pending"),
            AIDiagnosis(patient_id="P005", finding="Normal, age-appropriate", confidence=0.98, status="Done"),
        ]:
            s.add(d)
        for v in [
            VitalSign(patient_id="P001", heart_rate=72, blood_pressure="120/80", spo2=98),
            VitalSign(patient_id="P002", heart_rate=68, blood_pressure="118/76", spo2=99),
            VitalSign(patient_id="P003", heart_rate=85, blood_pressure="135/88", spo2=96),
            VitalSign(patient_id="P004", heart_rate=64, blood_pressure="110/70", spo2=99),
            VitalSign(patient_id="P005", heart_rate=78, blood_pressure="128/82", spo2=97),
        ]:
            s.add(v)
        # Aviation（中身を濃く）
        for f in [
            Flight(flight_id="JL001", route="NRT-LAX", departure="09:00", arrival="04:00", status="OnTime", aircraft="B777"),
            Flight(flight_id="NH002", route="HND-SFO", departure="10:30", arrival="05:30", status="OnTime", aircraft="B787"),
            Flight(flight_id="JL003", route="NRT-SIN", departure="14:00", arrival="20:30", status="Delayed", aircraft="B737"),
            Flight(flight_id="NH004", route="HND-LHR", departure="18:00", arrival="11:00", status="OnTime", aircraft="B777"),
            Flight(flight_id="JL005", route="NRT-HKG", departure="08:00", arrival="12:30", status="OnTime", aircraft="B767"),
            Flight(flight_id="NH006", route="HND-SEL", departure="13:15", arrival="15:45", status="Boarding", aircraft="B737"),
        ]:
            s.merge(f)
        for a in [
            Airport(code="NRT", departures_today=156, arrivals_today=148, congestion="Medium", weather="Clear"),
            Airport(code="HND", departures_today=412, arrivals_today=398, congestion="High", weather="Clear"),
            Airport(code="KIX", departures_today=98, arrivals_today=92, congestion="Low", weather="Cloudy"),
            Airport(code="NGO", departures_today=45, arrivals_today=42, congestion="Low", weather="Clear"),
        ]:
            s.merge(a)
        # Space（中身を濃く）
        for sat in [
            Satellite(satellite_id="ISS", name="International Space Station", orbit_km=408, inclination=51.6, period_min=92.9, status="Active"),
            Satellite(satellite_id="HUBBLE", name="Hubble Space Telescope", orbit_km=547, inclination=28.5, period_min=96.0, status="Active"),
            Satellite(satellite_id="STARLINK-001", name="Starlink 001", orbit_km=550, inclination=53.0, period_min=96.2, status="Active"),
            Satellite(satellite_id="LANDSAT-9", name="Landsat 9", orbit_km=705, inclination=98.2, period_min=99.0, status="Active"),
            Satellite(satellite_id="GOES-18", name="GOES-18", orbit_km=35786, inclination=0.0, period_min=1436, status="Active"),
        ]:
            s.merge(sat)
        for l in [
            Launch(launch_id="L001", mission="ISS Supply", launch_date="2026-03-15", vehicle="Falcon 9", status="Scheduled"),
            Launch(launch_id="L002", mission="Lunar Lander", launch_date="2026-04-20", vehicle="SLS", status="Scheduled"),
            Launch(launch_id="L003", mission="Starlink Batch", launch_date="2026-03-10", vehicle="Falcon 9", status="Completed"),
        ]:
            s.merge(l)
        s.commit()
    print("Seed done.")


if __name__ == "__main__":
    try:
        seed()
    except Exception as e:
        print(f"Seed failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
