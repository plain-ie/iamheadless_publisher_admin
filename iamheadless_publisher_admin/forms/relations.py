from django import forms
from django.forms import formset_factory
from django.forms import widgets


class RelationForm(forms.Form):

    direction = forms.CharField(initial='parent', widget=widgets.HiddenInput())
    item_id = forms.CharField(widget=widgets.HiddenInput())
    status = forms.CharField(widget=widgets.HiddenInput())
    title = forms.CharField(disabled=True, required=False)


RelationFormSet = formset_factory(RelationForm, extra=0)
