from django.conf.urls import url
from .views import check_eligibility_view

app_name = 'eligibility'
urlpatterns = [
    url(r'^check_eligibility/', check_eligibility_view, name='check_eligibility')
]