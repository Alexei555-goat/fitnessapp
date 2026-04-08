import sqlite3
from datetime import date

DB_NAME = "Galaburda_Alexei_fitnessstudio.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabellen anlegen
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Trainer (
            trainer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            vorname      TEXT    NOT NULL,
            nachname     TEXT    NOT NULL,
            spezialgebiet TEXT   NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Kurs (
            kurs_id          INTEGER PRIMARY KEY AUTOINCREMENT,
            bezeichnung      TEXT    NOT NULL,
            wochentag        TEXT    NOT NULL,
            uhrzeit          TEXT    NOT NULL,
            max_teilnehmer   INTEGER NOT NULL,
            trainer_id       INTEGER NOT NULL,
            FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
        );

        CREATE TABLE IF NOT EXISTS Mitglied (
            mitglied_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            vorname         TEXT    NOT NULL,
            nachname        TEXT    NOT NULL,
            email           TEXT    NOT NULL UNIQUE,
            beitrittsdatum  TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Anmeldung (
            anmeldung_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            mitglied_id     INTEGER NOT NULL,
            kurs_id         INTEGER NOT NULL,
            anmeldedatum    TEXT    NOT NULL,
            FOREIGN KEY (mitglied_id) REFERENCES Mitglied(mitglied_id),
            FOREIGN KEY (kurs_id)     REFERENCES Kurs(kurs_id),
            UNIQUE (mitglied_id, kurs_id)
        );
    """)

    # Beispieldaten: Trainer
    trainer = [
        ("Maria",  "Hoffmann",  "Yoga & Pilates"),
        ("Jonas",  "Bauer",     "Cycling & Ausdauer"),
        ("Sophie", "Keller",    "Tanz & Aerobic"),
    ]
    cursor.executemany(
        "INSERT INTO Trainer (vorname, nachname, spezialgebiet) VALUES (?, ?, ?)",
        trainer
    )

    # Beispieldaten: Kurse
    kurse = [
        ("Yoga",     "Montag",     "09:00", 15, 1),
        ("Pilates",  "Mittwoch",   "10:30", 12, 1),
        ("Spinning", "Dienstag",   "18:00", 20, 2),
        ("Spinning", "Donnerstag", "07:00", 20, 2),
        ("Zumba",    "Freitag",    "17:30", 25, 3),
        ("Aerobic",  "Samstag",    "11:00", 18, 3),
    ]
    cursor.executemany(
        "INSERT INTO Kurs (bezeichnung, wochentag, uhrzeit, max_teilnehmer, trainer_id) VALUES (?, ?, ?, ?, ?)",
        kurse
    )

    # Beispieldaten: Mitglieder
    mitglieder = [
        ("Lena",    "Müller",    "lena.mueller@email.at",    "2024-01-15"),
        ("Tobias",  "Schneider", "tobias.schneider@email.at","2024-02-03"),
        ("Anna",    "Fischer",   "anna.fischer@email.at",    "2024-03-20"),
        ("Markus",  "Weber",     "markus.weber@email.at",    "2024-04-11"),
        ("Julia",   "Meyer",     "julia.meyer@email.at",     "2024-05-08"),
        ("Felix",   "Wagner",    "felix.wagner@email.at",    "2024-06-01"),
        ("Laura",   "Braun",     "laura.braun@email.at",     "2024-07-22"),
    ]
    cursor.executemany(
        "INSERT INTO Mitglied (vorname, nachname, email, beitrittsdatum) VALUES (?, ?, ?, ?)",
        mitglieder
    )

    # Beispieldaten: Anmeldungen (mitglied_id, kurs_id, anmeldedatum)
    anmeldungen = [
        (1, 1, "2024-01-20"),   # Lena   -> Yoga
        (1, 3, "2024-01-22"),   # Lena   -> Spinning Di
        (2, 3, "2024-02-05"),   # Tobias -> Spinning Di
        (2, 4, "2024-02-06"),   # Tobias -> Spinning Do
        (3, 2, "2024-03-21"),   # Anna   -> Pilates
        (3, 5, "2024-03-23"),   # Anna   -> Zumba
        (4, 6, "2024-04-12"),   # Markus -> Aerobic
        (5, 1, "2024-05-09"),   # Julia  -> Yoga
        (5, 5, "2024-05-10"),   # Julia  -> Zumba
        (6, 2, "2024-06-02"),   # Felix  -> Pilates
        (7, 6, "2024-07-23"),   # Laura  -> Aerobic
    ]
    cursor.executemany(
        "INSERT INTO Anmeldung (mitglied_id, kurs_id, anmeldedatum) VALUES (?, ?, ?)",
        anmeldungen
    )

    conn.commit()
    print(f"Datenbank '{DB_NAME}' erfolgreich erstellt.")

    # Kurze Übersicht zur Kontrolle
    print("\n--- Trainer ---")
    for row in cursor.execute("SELECT * FROM Trainer"):
        print(row)

    print("\n--- Kurse ---")
    for row in cursor.execute("""
        SELECT k.kurs_id, k.bezeichnung, k.wochentag, k.uhrzeit,
               k.max_teilnehmer, t.vorname || ' ' || t.nachname AS trainer
        FROM Kurs k JOIN Trainer t ON k.trainer_id = t.trainer_id
    """):
        print(row)

    print("\n--- Mitglieder ---")
    for row in cursor.execute("SELECT * FROM Mitglied"):
        print(row)

    print("\n--- Anmeldungen ---")
    for row in cursor.execute("""
        SELECT a.anmeldung_id,
               m.vorname || ' ' || m.nachname AS mitglied,
               k.bezeichnung AS kurs,
               a.anmeldedatum
        FROM Anmeldung a
        JOIN Mitglied m ON a.mitglied_id = m.mitglied_id
        JOIN Kurs     k ON a.kurs_id     = k.kurs_id
        ORDER BY a.anmeldedatum
    """):
        print(row)

    conn.close()

if __name__ == "__main__":
    create_database()