from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from django.utils import timezone
import datetime

class Service(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Facility(models.Model):
    facilityty=(('Specialized','Specialized'),('General','General'),('Primary','Primary'),('Health Center','Health Center'))
    facility_type = models.CharField(choices=facilityty,max_length=30)
    facility_name = models.CharField(max_length=25)
    reg = (('ADDIS ABBABA','ADDIS ABBABA'),('OROMIA','OROMIA'),('AMHARA','AMHARA'),('TIGRAY','TIGRAY'),('SOUTH','SOUTH'),('GAMBELLA','GAMBELLA'),('BENSHANGUL','BENSHANGUL'),('HARRARI','HARRARI'),('DIREDAWA','DIREDAWA'),('SIDAMA','SIDAMA'),('SOUTH WEST','SOUTH WEST'))
    region = models.CharField(choices=reg, max_length=50)
    subcity = models.CharField(max_length=25)
    woreda = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    def __str__(self):
       return self.facility_name

class Facility_User(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=False)
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE, default=1)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_phone(self):
        return self.mobile   
    @property
    def get_facility(self):
        return self.facility.facility_name 
    def __str__(self):
        return self.user.first_name

class ReferTo(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    refer_to = models.PositiveIntegerField()
    def __str__(self):
        return self.facility.facility_name

class RegionalAdmin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    reg = (('ADDIS ABBABA','ADDIS ABBABA'),('OROMIA','OROMIA'),('AMHARA','AMHARA'),('TIGRAY','TIGRAY'),('SOUTH','SOUTH'),('GAMBELLA','GAMBELLA'),('BENSHANGUL','BENSHANGUL'),('HARRARI','HARRARI'),('DIREDAWA','DIREDAWA'),('SIDAMA','SIDAMA'),('SOUTH WEST','SOUTH WEST'))
    region = models.CharField(choices=reg, max_length=50)
    status=models.BooleanField(default=False)
  
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class Liaizon(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE, default=1)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_phone(self):
        return self.mobile
    
    @property
    def get_facility(self):
        return self.facility.facility_name
   
    def __str__(self):
        return self.user.first_name


class CEO(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE, default=1)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

def is_valid_queryparam(param):
    return param !='' and param is not None
class referalrequest(models.Model):
    typeor = (('COLD','COLD'),('EMERGENCY','EMERGENCY'))
    type_of_referal = models.CharField(choices=typeor,max_length=30)
    name_of_patient = models.CharField(max_length=50)
    gen = (('MALE','MALE'),('FEMALE','FEMALE'))
    paient_age = models.CharField(max_length=10)
    gender = models.CharField(choices=gen,max_length=10)
    reg = (('ADDIS ABBABA','ADDIS ABBABA'),('OROMIA','OROMIA'),('AMHARA','AMHARA'),('TIGRAY','TIGRAY'),('SOUTH','SOUTH'),('GAMBELLA','GAMBELLA'),('BENSHANGUL','BENSHANGUL'),('HARRARI','HARRARI'),('DIREDAWA','DIREDAWA'),('SIDAMA','SIDAMA'),('SOUTH WEST','SOUTH WEST'))
    patient_region = models.CharField(choices=reg ,max_length=35)
    patient_subcity = models.CharField(max_length=25)
    patient_woreda = models.CharField(max_length=25)
    patient_phone = models.CharField(max_length=25)
    chief_compliants = models.CharField(max_length=30)
    diagnosis = models.CharField(max_length=30)
    required_service = models.ForeignKey(Service,on_delete=models.CASCADE)
    reason_for_referal =models.CharField(max_length=40)
    refering_dr = models.CharField(max_length=25)
    dr_phone = models.CharField(max_length=30)
    bloty =(('A' ,'A'),('B','B') ,('O','O') ,('A+','A+'),('A-','A-'),('AB-','AB-'),('AB+','AB+'),('O-','O-'))
    blood_type = models.CharField(max_length=40,choices=bloty)
    bt_choices = (('YES','YES'),('NO','NO'))
    blood_transfusion = models.CharField(max_length=40,choices=bt_choices,blank=True,null=True)
    ambulance_driver_name = models.CharField(max_length=25)
    ambulance_driver_phone = models.CharField(max_length=20)
    ahp_name = models.CharField(max_length=25)
    ahp_phone = models.CharField(max_length=25)
    refered_date = models.DateTimeField(auto_now_add=True)
    
    pd = (('THE SAME TO REFERING FACILITY','THE SAME TO REFERAL FACILLITY'),
          ('NOT THE SAME TO REFERING FACILITY','NOT THE SAME TO REFERING FACILITY'))
    patient_diagnosis = models.CharField(choices=pd,max_length=40,null=True,blank=True)
    comments_of_referal = models.TextField(max_length=250,null=True,blank=True)
    wrtm = (('YES','YES'),('NO','NO'))
    with_respect_to_medical_care = models.CharField(choices=wrtm,max_length=5,null=True,blank=True)
    # patient_diagnosis = models.CharField(max_length=15,null=True,blank=True)
    wrpt = (('YES','YES'),('NO','NO'))
    with_respect_patient_transportation = models.CharField(choices=wrpt,max_length=5,null=True,blank=True)

    stat = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Feedback', 'Feedbak'), ('Re-direct', 'Re-direct'))
    status = models.CharField(max_length=50, choices=stat, default='Pending', null=True)
    referal_to = models.ForeignKey('Facility',on_delete=models.CASCADE)
    liaizon=models.ForeignKey('Liaizon',related_name='refered_by', on_delete=models.CASCADE,null=True,blank=True)
    approved_date = models.DateTimeField(null=True,blank=True)
    approved_by=models.ForeignKey('Liaizon',related_name='approved_by', on_delete=models.CASCADE,null=True,blank=True)
    feedback_date = models.DateTimeField(null=True,blank=True)
    feedback_by=models.ForeignKey('Liaizon',related_name='feedback_by', on_delete=models.CASCADE,null=True,blank=True)
    re_referal_date = models.DateTimeField(null=True,blank=True)
    re_referal_by=models.ForeignKey('Liaizon',related_name='re_referal_by', on_delete=models.CASCADE,null=True,blank=True)
    reason_for_rereferal = models.CharField(max_length=200,null=True,blank=True)
        
    @property
    def get_approved_day_count(self):
        if is_valid_queryparam(self.approved_date):
            # return (self.approved_date - self.refered_date).time
            return (self.approved_date - self.refered_date)
        else:
            return ""
            # return convert_timedelta(timezone.now() - self.refered_date)
            # return (self.datetime.now() - self.refered_date)/3600
    @property
    def get_feedback_date_day_count(self):
        if is_valid_queryparam(self.feedback_date) and is_valid_queryparam(self.approved_date):
            return (self.feedback_date - self.approved_date)
        else:
            return ""
            # return convert_timedelta(timezone.now() - self.refered_date )
    @property
    def get_re_referal_date_day_count(self):
        if is_valid_queryparam(self.re_referal_date):
            return (self.re_referal_date - self.approved_date)
            # return convert_timedelta(self.re_referal_date - self.approved_date)
        else:
            return ""
            # return convert_timedelta(timezone.now() - self.approved_date)
       
                
class Ward(models.Model):
    ward_type = models.CharField(max_length=50)
    ward_name = models.CharField(max_length=50)
    created_by = models.ForeignKey('Facility_User',on_delete=models.CASCADE)
    facility_id = models.ForeignKey('Facility',on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.ward_name

class Facility_Service(models.Model):
    service_name = models.CharField(max_length=50)
    service_desc = models.CharField(max_length=200)
    created_by = models.ForeignKey('Facility_User',on_delete=models.CASCADE)
    facility = models.ForeignKey('Facility',on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.ward_name

class Room(models.Model):
    ward = models.ForeignKey('Ward',on_delete=models.CASCADE,default=1)
    room_no = models.CharField(max_length=50)
    gen = (('Male','Male'),('Female','Female'),('Both','Both'))
    room_type = models.CharField(max_length=50, choices=gen, null=True)
    no_beds = models.PositiveIntegerField()
    occ_beds = models.PositiveIntegerField()
    free_beds = models.PositiveIntegerField()
    created_by = models.ForeignKey('Facility_User',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    facility = models.ForeignKey('Facility',on_delete=models.CASCADE)
    def __str__(self):
       return self.room_no

class Patient(models.Model):
    mrn = models.CharField(max_length=50,null=True,blank=True) 
    fname = models.CharField(max_length=50,null=True,blank=True)
    mob = models.CharField(max_length=50,null=True,blank=True)
    facility_id = models.ForeignKey('Facility',on_delete=models.CASCADE,null=True,blank=True)
    created_by = models.ForeignKey('Facility_User',on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    patient_mrn = models.CharField(max_length=50) 
    patient_name = models.CharField(max_length=50)
    gen = (('Male','Male'),('Female','Female'))
    gender = models.CharField(max_length=50, choices=gen, null=True)
    patient_age = models.CharField(max_length=4)
    mob = models.CharField(max_length=50)
    diagnosis = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    app_date = models.DateField()
    app_round = models.CharField(max_length=50)
    reason = models.CharField(max_length=200)
    stat = (('Pending', 'Pending'), ('Admitted', 'Admitted'), ('Not Available', 'Not Available'))
    status = models.CharField(max_length=50, choices=stat, default='Pending', null=True)
    facility = models.ForeignKey('Facility',on_delete=models.CASCADE)
    created_by = models.ForeignKey('Facility_User',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.patient_name

class Appoint(models.Model):
    patient_mrn = models.CharField(max_length=50)
    patient_name = models.CharField(max_length=200)
    gen = (('Male','Male'),('Female','Female'))
    gender = models.CharField(max_length=50, choices=gen, null=True)
    patient_age = models.CharField(max_length=50)
    mob = models.CharField(max_length=50)
    diagnosis = models.TextField()
    department = models.CharField(max_length=50)
    reason = models.TextField()
    app_date = models.DateTimeField()
    stat = (('Pending', 'Pending'), ('Waiting', 'Waiting'), ('Admitted', 'Admitted'),('Not Available','Not Available'),('Re-Appointed','Re-Appointed'))
    status = models.CharField(max_length=50, choices=stat, default='Waiting', null=True)
    app_round = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey('Facility_User',on_delete=models.CASCADE)
    facility = models.ForeignKey('Facility',on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.patient_name

# class Appointment(models.Model):
#     patient_mrn = models.CharField(max_length=50) 
#     patient_name = models.CharField(max_length=50)
#     gen = (('Male','Male'),('Female','Female'))
#     patient_age = models.CharField(max_length=10)
#     mob = models.CharField(max_length=50)
#     diagnosis = models.CharField(max_length=50)
#     department = models.CharField(max_length=50)
#     app_date = models.DateTimeField(null=True,blank=True)
#     reason = models.CharField(max_length=200)
#     stat = (('Pending', 'Pending'), ('Waiting', 'Approved'), ('Feedback', 'Feedbak'), ('Re-direct', 'Re-direct'))
#     status = models.CharField(max_length=50, choices=stat, default='Pending', null=True)
#     facility_id = models.ForeignKey('Facility',on_delete=models.CASCADE)
#     created_by = models.ForeignKey('Facility_User',on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.patient_name
