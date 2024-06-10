from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    count = forms.IntegerField(label="Count", min_value=1)
    file = forms.FileField(label='Select an Excel file', help_text='Only .xlsx files are allowed.',
                           widget=forms.FileInput(attrs={'accept': '.xlsx'}))