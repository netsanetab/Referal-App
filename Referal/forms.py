from django import forms
from django.contrib.auth.models import User
from . import models

class LiaizonUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class LiaizonForm(forms.ModelForm):
   
    class Meta:
          model=models.Liaizon
          fields=['address','mobile','facility']

class RegionalAdminUserForm(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['first_name','last_name','username','password']
        wdgets = {
            'password': forms.PasswordInput()
        }
class RegionalAdminForm(forms.ModelForm):
    class Meta:
        model=models.RegionalAdmin
        fields=['region']

class ReferalRequestForm(forms.ModelForm):
    # assignedHospitalID = forms.ModelChoiceField(queryset=models.hospital.objects.all(), empty_label="select Hospitals", to_field_name="id")
    class Meta:
        model=models.referalrequest
        fields=['type_of_referal','name_of_patient','paient_age','patient_region','patient_subcity','patient_woreda','patient_phone',
        'chief_compliants','diagnosis','required_service',
          'reason_for_referal','refering_dr','ambulance_driver_name','ambulance_driver_phone','ahp_name','ahp_phone','referal_to']
class LiaizonApproveRequestForm(forms.Form):
     pd = (('THE SAME TO REFERING FACILITY', 'THE SAME TO REFERAL FACILLITY'),
           ('NOT THE SAME TO REFERING FACILITY', 'NOT THE SAME TO REFERING FACILITY'))
     patient_diagnosis = forms.ChoiceField(choices=pd)
     comments_of_referal = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

     se = (('YES', 'YES'), ('NO', 'NO'))
     with_respect_to_medical_care = forms.ChoiceField(choices=se)
     sel = (('YES', 'YES'), ('NO', 'NO'))
     with_respect_patient_transportation = forms.ChoiceField(choices=sel)

class liaizonApproveRequestForm(forms.Form):
    stat = (('Pending','Pending'),('Approved','Approved'))
    status = forms.ChoiceField(choices=stat)