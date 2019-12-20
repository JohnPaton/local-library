import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks from now (default 3)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        # Not in the past
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in the past"))

        # Not more than 4 weeks from now
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _("Invalid date - renewal more than 4 weeks ahead")
            )

        return data


# ModelForms provide a lot of config "for free" if you have models
# with many fields (not much added value in this case)
class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ["due_back"]
        labels = {"due_back": _("New renewal date")}
        help_texts = {
            "due_back": _("Enter a date between now and 4 weeks (default 3).")
        }

    def clean_due_back(self):
        data = self.cleaned_data["due_back"]

        # Not in the past
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in the past"))

        # Not more than 4 weeks from now
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _("Invalid date - renewal more than 4 weeks ahead")
            )

        return data
