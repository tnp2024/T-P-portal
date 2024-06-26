from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name
    

    
class Drive(models.Model):

    DRIVE_STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Active', 'Active'),
        ('Upcoming', 'Upcoming'),
    ]

    Reference_no = models.CharField(max_length=100)     
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=30)
    company_logo = models.ImageField(null=True,blank=True,upload_to='logos/')
    date = models.DateField()
    application_last_date = models.DateField(default='2002-12-02')
    content = models.TextField()
    Bond = models.CharField(max_length=50)
    industry_type = models.CharField(max_length=50) 
    department = models.ManyToManyField(Department)
    job_role = models.CharField(max_length=50)
    job_location = models.CharField(max_length=50)
    job_eligibility = models.TextField()
    job_description = models.TextField()
    job_CTC = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    drive_id = models.AutoField(primary_key=True)
    application_link = models.CharField(max_length=100,null=True,blank=True)
    resume_link = models.CharField(max_length=200, blank=True)
    num_rounds = models.IntegerField(default=1, verbose_name='Number of Rounds')
    round1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Round 1 Name',default ='Round 1')
    round2 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Round 2 Name')
    round3 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Round 3 Name')
    round4 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Round 4 Name')
    round5 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Round 5 Name')
    drive_status = models.CharField(max_length=10, choices=DRIVE_STATUS_CHOICES, default='Upcoming')

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if self.date == today:
            self.drive_status = 'Active'
        elif self.date > today:
            self.drive_status = 'Upcoming'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-creation_date']
    
  


from django.db import models

class Activity(models.Model):      

    ACTIVITY_STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Active', 'Active'),
        ('Upcoming', 'Upcoming'),
    ]
    Reference_no = models.CharField(max_length=100)  
    activity_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    company_logo = models.ImageField(null=True,blank=True,upload_to='logos/')
    company_name = models.CharField(max_length=255)
    industry_type = models.CharField(max_length=255)
    activity_date = models.DateField()
    department = models.ManyToManyField(Department)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True)
    activity_status = models.CharField(max_length=10, choices=ACTIVITY_STATUS_CHOICES, default='Upcoming')

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if self.activity_date == today:
            self.activity_status = 'Active'
        elif self.activity_date > today:
            self.activity_status = 'Upcoming'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-creation_date']

  

class Booklets(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    booklet = models.FileField(upload_to='booklets/')
    department = models.ManyToManyField(Department)
    company_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    company_logo = models.ImageField(null=True, blank=True, upload_to='logos/')

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['creation_date']
