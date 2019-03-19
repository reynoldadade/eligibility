from django.db import models


class GovEmployee(models.Model):
    emp_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=50)
    dob = models.DateField()
    assignment_status = models.CharField(max_length=30)
    gender = models.CharField(max_length=6)
    job = models.CharField(max_length=74)
    organization = models.CharField(max_length=80)
    hire_date = models.DateField()
    department = models.CharField(max_length=59)
    ministry = models.CharField(max_length=49)
    ssn = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=34)
    bank_branch = models.CharField(max_length=60)
    account_number = models.CharField(max_length=60)
    location = models.CharField(max_length=20)
    district = models.CharField(max_length=46)
    region = models.CharField(max_length=20)
    ssn_exempt = models.CharField(max_length=1)
    pupil_teacher_status = models.CharField(max_length=1)
    teacher_trainee_status = models.CharField(max_length=1)
    phoneNumber = models.CharField(max_length=20)
    phoneNumber2 = models.CharField(max_length=20)

    # blacklisted = models.CharField(max_length=3)
    #
    # class Meta:
    #     permissions = (
    #         ("view_blacklist", "Can view Blacklist button"),
    #         ("view_whitelist", "Can view Whitelist button"),
    #     )

    def __str__(self):
        return self.emp_id


class Quote(models.Model):
    text = models.CharField(max_length=300)
    author = models.CharField(max_length=60)
