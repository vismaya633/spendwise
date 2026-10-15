from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from spending.serializers import UserSerializer,ExpenseSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import authentication,permissions
from spending.models import Expense
from spending.permissions import IsOwner

from spending.ai_service import get_budget_plan

from datetime import datetime
from django.db.models import Sum
# Create your views here.

class SignupView(APIView):

    def post(self,request):

        form_data=request.data

        serializer_instance=UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data=serializer_instance.validated_data

            instance=User.objects.create_user(**cleaned_data)

            serializer_instance=UserSerializer(instance)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        

class GetMeView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get (self,request):
        auth_user=request.user
        instance=User.objects.get(username=auth_user)
        serializer_instance=UserSerializer(instance)
        return Response(data=serializer_instance.data)
    

class ExpenseListCreateView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        instance=Expense.objects.filter(owner=request.user)

        serializer_instance=ExpenseSerializer(instance,many=True)

        return Response(data=serializer_instance.data)
    
    def post(self,request):

        form_data=request.data

        serializer_instance=ExpenseSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data=serializer_instance.validated_data

            instance=Expense.objects.create(**cleaned_data,owner=request.user)

            serializer_instance=ExpenseSerializer(instance)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
class ExpenseRetreiveUpdateDeleteView(APIView):


    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]

    def get(self,request,pk=None):

        instance=Expense.objects.get(id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance=ExpenseSerializer(instance)

        return Response(data=serializer_instance.data)
    
    def put(self,request,pk=None):

        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        form_data=request.data

        serializer_instance=ExpenseSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        

    def delete(self,request,pk=None):

        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"deleted"})
    

class ExpenseSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={
            "todays_total":0
        }


        cur_date=datetime.now().date()
        cur_month=datetime.now().month
        cur_year=datetime.now().year

        #monthly summary

        
        cur_month_transaction = Expense.objects.filter(owner=request.user, created_at__month=cur_month, created_at__year=cur_year)
        if  cur_month_transaction:
            monthly_total=cur_month_transaction.values("amount").aggregate(total=Sum("amount")).get("total")
            response_data={
                "monthly_total":monthly_total
            }

            monthly_total=cur_month_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            category_summary=todays_transaction.values("category").annotate(total=Sum("amount"))



        todays_transaction=Expense.objects.filter(owner=request.user,created_at__date=cur_date)

        if todays_transaction:

            todays_total=todays_transaction.values("amount").aggregate(total=Sum("amount")).get("total")


            category_summary=todays_transaction.values("category").annotate(total=Sum("amount"))

            

            response_data={"todays_total":todays_total}

            response_data={"category_summary":category_summary}

        return Response(data=response_data)
    

class BudgetPlanView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        user=request.user

        
        cur_year=datetime.now().year
        cur_month=datetime.now().month

        response_data={
            "monthly_total":0
        }

        monthly_transaction=Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        if monthly_transaction:

            monthly_total=monthly_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            monthly_category_summary = monthly_transaction.values("category").annotate(total=Sum("amount"))

            response_data["monthly_total"] = monthly_total
            response_data["category_summary"] = monthly_category_summary

            

            

            get_budget_plan(response_data)

        return Response(data=response_data)




