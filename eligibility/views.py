from __future__ import division
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import IDSearchForm
from .models import GovEmployee
from datetime import date, datetime
from math import floor


@login_required
def check_eligibility_view(request):
    current_time = datetime.now()
    if current_time.hour < 12:
        greeting = "Good Morning"
    elif current_time.hour >= 12 and current_time.hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    lts = [3] + [6 * i for i in range(1, 10)]
    lts.reverse()
    form_issue = False
    dne = False
    emp = None
    age = None
    reason = None
    max_loan_tenor = None
    blacklisted = None

    if request.method == "POST":
        form = IDSearchForm(data=request.POST)
        if form.is_valid():
            emp_id = form.cleaned_data['emp_id']
            emp_id = emp_id.strip().upper()
            try:
                emp = GovEmployee.objects.get(emp_id=emp_id)
                today = date.today()
                dob = emp.dob
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if dob.month == 2 and dob.day == 29:
                    try:
                        date_will_be_57 = date(year=dob.year + 57, month=dob.month, day=dob.day)
                    except:
                        date_will_be_57 = date(year=dob.year + 57, month=dob.month, day=dob.day - 1)
                else:
                    date_will_be_57 = date(year=dob.year + 57, month=dob.month, day=dob.day)

                months_left = floor(((date_will_be_57 - today).days / 365) * 12)

                if (emp.assignment_status == "ACTIVE" and emp.blacklisted == "No"):
                    if (emp.ssn == "NONE" or emp.ssn == "0" or emp.ssn == "") and emp.ssn_exempt == "Y":
                        if age >= 57:
                            reason = "The employee is {0} years old.".format(age)
                        elif months_left < 3:
                            reason = 'The employee will turn 57 in less than 3 months.'
                        else:
                            for lt in lts:
                                if lt <= months_left:
                                    max_loan_tenor = "{0} months".format(lt)
                                    break

                    elif (emp.ssn == "NONE" or emp.ssn == "0" or emp.ssn == "") and emp.ssn_exempt == "N":
                        reason = "The employee has no SSN and is not part of the exempted class."

                    else:
                        if emp.pupil_teacher_status == "Y":
                            if age >= 57:
                                reason = "The employee is {0} years old".format(age)
                            elif months_left < 3:
                                reason = 'The employee will turn 57 in less than 3 months.'
                            elif months_left >= 24:
                                max_loan_tenor = "24 months"
                            else:
                                for lt in lts:
                                    if lt <= months_left:
                                        max_loan_tenor = "{0} months".format(lt)
                                        break

                        elif emp.teacher_trainee_status == "Y" and (emp.hire_date <= date(year=2012, month=9, day=1)):
                            if age >= 57:
                                reason = "The employee is {0} years old.".format(age)
                            elif months_left < 3:
                                reason = 'The employee will turn 57 in less than 3 months.'
                            else:
                                for lt in lts:
                                    if lt <= months_left:
                                        max_loan_tenor = "{0} months".format(lt)
                                        break

                        elif emp.teacher_trainee_status == "Y" and (emp.hire_date > date(year=2012, month=9, day=1)):
                            reason = "The employee is a teacher trainee employed after Sept 1 2012."
                        else:
                            if age >= 57:
                                reason = "The employee is {0} years old.".format(age)
                            elif months_left < 3:
                                reason = 'The employee will turn 57 in less than 3 months.'
                            else:
                                for lt in lts:
                                    if lt <= months_left:
                                        max_loan_tenor = "{0} months".format(lt)
                                        break
                elif (emp.assignment_status == "ACTIVE" and emp.blacklisted == "Yes"):
                    blacklisted = True
                else:
                    reason = "The employee is NOT ACTIVE."
            except GovEmployee.DoesNotExist:
                dne = True

        else:
            form_issue = True

    context = {}
    context['blacklisted'] = blacklisted
    context['greeting'] = greeting
    context['form_issue'] = form_issue
    context['dne'] = dne
    context['emp'] = emp
    context['age'] = age
    context['reason'] = reason
    context['max_loan_tenor'] = max_loan_tenor

    return render(request, 'eligibility/check_eligibility.html', context)
