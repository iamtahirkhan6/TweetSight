from django import forms
   
# creating a form 
class RunToolForm(forms.Form):
    username = forms.CharField(max_length = 15)