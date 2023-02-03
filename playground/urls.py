from django.urls import path
from . import views

#django looks for this variable
#URL Conf : 
urlpatterns = [path(route="test1/" ,view=views.landing_page)] 
# path always ends with a forwards slash 
# return URLPattern object