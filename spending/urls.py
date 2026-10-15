


from django.urls import path
from spending.views import SignupView
from spending.views import GetMeView
from spending.views import ExpenseListCreateView
from spending.views import ExpenseRetreiveUpdateDeleteView
from rest_framework.authtoken.views import ObtainAuthToken
from spending.views import ExpenseSummaryView
from spending.views import BudgetPlanView

urlpatterns=[
path("register/",SignupView.as_view()),
path("me/",GetMeView.as_view()),
path("expense/",ExpenseListCreateView.as_view()),
path("expense/<int:pk>/",ExpenseRetreiveUpdateDeleteView.as_view()),
path("token/",ObtainAuthToken.as_view()),
path("expense/summary/",ExpenseSummaryView.as_view()),
path("budget/",BudgetPlanView.as_view()),


]