from django import forms

class SearchForm(forms.Form):
    # TODO should of same type as the database
    source = forms.MultipleChoiceField()
    destination = forms.CharField(max_length=100)
    departure = forms.DateTimeField()
    arrival = forms.DateTimeField()
    search_type = forms.ChoiceField(choices=[('departure', 'Departure'), ('arrival', 'Arrival')])