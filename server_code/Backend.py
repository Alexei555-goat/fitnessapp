import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def query_database(query: str):
  with sqlite3.connect(data_files["Galaburda_Alexei_fitnessstudio.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result

@anvil.server.callable
def query_kurs_database():
  query = """
        SELECT 
            k.bezeichnung,
            k.wochentag,
            k.uhrzeit,
            t.vorname || ' ' || t.nachname AS trainer,
            COUNT(a.anmeldung_id) || '/' || k.max_teilnehmer AS teilnehmer
        FROM Kurs k
        LEFT JOIN Trainer t ON t.trainer_id = k.trainer_id
        LEFT JOIN Anmeldung a ON a.kurs_id = k.kurs_id
        GROUP BY k.kurs_id
        ORDER BY k.bezeichnung
    """
  return query_database(query)

@anvil.server.callable
def query_mitglied_database(kurs):
  query = f"""
            SELECT
                m.vorname,
                m.nachname
            FROM Mitglied m
            JOIN Anmeldung a ON a.mitglied_id = m.mitglied_id
            JOIN Kurs k ON k.kurs_id = a.kurs_id
            WHERE k.bezeichnung = '{kurs}'
        """
  return query_database(query)

@anvil.server.callable
def query_anmeldenmitgleid_database(kurs):
  query = f"""
        SELECT 
            m.mitglied_id,
            m.vorname || ' ' || m.nachname AS name,
            k.kurs_id
        FROM Mitglied m, Kurs k
        WHERE k.bezeichnung = '{kurs}'
        AND m.mitglied_id NOT IN (
            SELECT a.mitglied_id 
            FROM Anmeldung a
            WHERE a.kurs_id = k.kurs_id
        )
    """
  return query_database(query)

@anvil.server.callable
def anmelden(mitglied_id, kurs_id):
  with sqlite3.connect(data_files["Galaburda_Alexei_fitnessstudio.db"]) as conn:
    cur = conn.cursor()
    cur.execute(
      "INSERT INTO Anmeldung (mitglied_id, kurs_id, anmeldedatum) VALUES (?, ?, ?)",
      (mitglied_id, kurs_id, datetime.date.today().isoformat())
    )
    conn.commit()
