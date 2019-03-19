from django import forms


class IDSearchForm(forms.Form):
    emp_id = forms.CharField(label='Employee_ID', max_length=50)

