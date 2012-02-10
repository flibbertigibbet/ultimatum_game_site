from tw.api import WidgetsList
from tw.forms import TableForm, SingleSelectField, Spacer, HiddenField


class AcceptOfferForm(TableForm):

    class fields(WidgetsList):
        game_id = HiddenField() 
        accept = SingleSelectField(options=['Yes', 'No'])
    

