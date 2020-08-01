from django import forms


class UploadFileForm(forms.Form):
    import_file = forms.FileField()
