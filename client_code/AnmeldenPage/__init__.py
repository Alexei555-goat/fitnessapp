from ._anvil_designer import AnmeldenPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AnmeldenPage(AnmeldenPageTemplate):
  def __init__(self, item, **properties):
    self.init_components(**properties)
    self.item = item
    self.load_mitglieder()

  def load_mitglieder(self):
    returnValue = anvil.server.call('query_anmeldenmitgleid_database', self.item["kurs"])
    data = []
    for v in returnValue:
      data.append({
        'mitglied_id': v[0],
        'mitglied':    v[1],
        'kurs_id':     v[2],
      })
    self.repeating_panel_anmelden.items = data

  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("MainPage")
    pass
