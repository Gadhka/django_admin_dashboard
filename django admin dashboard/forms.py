from django import forms
def GlobalForms(mymodel):
    class DynamicGlobalForm(forms.ModelForm):
        class Meta:
            model = mymodel
            fields = "__all__"
    return DynamicGlobalForm

