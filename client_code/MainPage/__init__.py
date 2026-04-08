from ._anvil_designer import MainPageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server as db


class MainPage(MainPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_kurse()

  def load_kurse(self):
    rows = db.call("query_kurs_database")
    
    data = []
    for v in rows:
      data.append({
        'kurs':       v[0],
        'wochentag':  v[1],
        'Uhrzeit':    v[2],
        'trainer':    v[3],
        'Teilnehmer': v[4],
      })
    self.repeating_panel_fitess.items = data