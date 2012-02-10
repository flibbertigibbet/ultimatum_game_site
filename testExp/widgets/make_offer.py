from tw.api import WidgetsList
from tw.forms import TableForm, SingleSelectField, Spacer, HiddenField

class MakeOfferForm(TableForm):
 
    class fields(WidgetsList):
        game_id = HiddenField()
        proposal_amt = SingleSelectField(options=range(1, 5), label_text='Offer Amount')

        


