from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from lookfinanz.models import *
from django.db import IntegrityError
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponse
import random
from datetime import date, timedelta
import json
from django.db import models
from django import forms
from django.db.models import F
from django import forms
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.db.models import Case, When, F, DecimalField
from django.contrib.auth.decorators import login_required

class TransactionDateRangeForm(forms.Form):
    begin = forms.DateField(
        label="Begin",
        widget=forms.SelectDateWidget(years=range(2020, 2031),attrs={'id': 'begin_id'}))

    end = forms.DateField(
        label="End",
        widget=forms.SelectDateWidget(years=range(2020, 2031),attrs={'id': 'end_id'}))


def random_date_2020_2025():
    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 31)

    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)

    return start_date + timedelta(days=random_days)

list_description=["a","b","c","d"]
list_period=[
    ['day','Day'],
    ['month','Month'],
    ['year','Year']
]
EXPENSE_CATEGORY_CHOICES = [
    ['rent', 'Rent'],
    ['food', 'Food'],
    ['transport', 'Transport'],
    ['health', 'Health'],
    ['entertainment', 'Entertainment'],
    ['education', 'Education'],
    ['bills', 'Bills'],
    ['shopping', 'Shopping'],
    ['taxes', 'Taxes'],
];

INCOME_CATEGORY_CHOICES = [
    ['salary', 'Salary'],
    ['freelance', 'Freelance'],
    ['interest', 'Interest'],
    ['dividends', 'Dividends'],
    ['gifts', 'Gifts'],
];
# Create your views here.
list_name=["carmel","herman","setphane","gervais"]
from django import forms
class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=["amount","description","transaction_type","name","category"]


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    all_transaction= Transaction.objects.filter(
        author=request.user
    ).order_by('-date')
    form = TransactionDateRangeForm()
    return render(request,"lookfinanz/index.html",{"all_transaction":all_transaction,"form":form,"user":request.user})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "lookfinanz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lookfinanz/login.html")
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lookfinanz/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
@login_required
def newtransaction(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Re
    if request.method=="POST":
       form = TransactionForm(request.POST)
       if form.is_valid():
           name=form.cleaned_data["name"]
           transaction_type = form.cleaned_data["transaction_type"]
           amount = form.cleaned_data["amount"]
           category= form.cleaned_data["category"]
           description = form.cleaned_data["description"]
           Transaction.objects.create(author=User.objects.get(id=request.user.id),transaction_type=transaction_type,amount=amount,category=category,name=name,description=description)
       else:
           return HttpResponse("pas valide")

    return render(request,"lookfinanz/newtransaction.html")

def random_data_upload(request):

    if request.method == "POST":
        data = json.loads(request.body)
        n = int(data.get("number"))

        for i in range(n):
            name = random.choice(list_name)
            date = random_date_2020_2025()
            description = random.choice(list_description)
            if i % 2 == 0:

                transaction_type = "income"
                category = random.choice(INCOME_CATEGORY_CHOICES)[0]
            else:
                transaction_type = "expense"
                category = random.choice(EXPENSE_CATEGORY_CHOICES)[0]
            amount = random.randint(1, 1000)
            Transaction.objects.create(name=name, date=date, description=description, transaction_type=transaction_type,
                                       category=category, amount=amount,author=request.user)
    return redirect("index")

def filter_data_of_index_page(request):
    if request.method=="POST":
       data = json.loads(request.body)
       if data["transaction_type"] !="all":
          transactions=Transaction.objects.filter(category=data["category"],transaction_type=data["transaction_type"],date__range=(data["begin"], data["end"]),author=request.user)
       else:
           transactions = Transaction.objects.filter(date__range=(data["begin"], data["end"]),author=request.user).order_by('-date')
       transactions_list = [t.serialize() for t in transactions]
       return JsonResponse(transactions_list ,safe=False)


def delete_transaction(request):
    if request.method=="PUT":
       data = json.loads(request.body)
       transaction_to_delete=Transaction.objects.get(id=data["id"])
       transaction_to_delete.delete()
       return JsonResponse({"message":True})

def update_transaction(request):
    if request.method=='PUT':
        data = json.loads(request.body)
        transactions=Transaction.objects.filter(id=data["id"]).update(transaction_type=data["type"],amount=data["amount"],category=data["category"],description=data["description"],name=data["name"])


        return JsonResponse({"message": True})


@login_required
def dashboard(request):
    if request.method=="POST":
       data = json.loads(request.body)
       transactions = Transaction.objects.filter(
           author=request.user,
           date__range=(data["begin"], data["end"])
       ).annotate(
           signed_amount=Case(
               When(transaction_type="expense", then=-F("amount")),
               default=F("amount"),
               output_field=DecimalField()
           )
       )

       transactions_expense=Transaction.objects.filter(date__range=(data["begin"], data["end"]),author=request.user)
       transactions_expense=transactions_expense.filter(transaction_type="expense")
       transactions_income = Transaction.objects.filter(date__range=(data["begin"], data["end"]),author=request.user)
       transactions_income=transactions_income.filter(transaction_type="income")

       if data["period"] == 'day':
           trunc_func = TruncDay('date')
       elif data["period"] == 'month':
           trunc_func = TruncMonth('date')
       elif data["period"] == 'year':
           trunc_func = TruncYear('date')

       transactions = (
           transactions
           .annotate(period=trunc_func)  # crée la colonne 'period'
           .values('period')  # ça fait le "GROUP BY period"
           .annotate(total=Sum('amount'))  # somme les montants pour chaque period
           .order_by('period')
       )
       transactions_income = (
           transactions_income
           .values('category')  # ça fait le "GROUP BY period"
           .annotate(total=Sum('amount'))  # somme les montants pour chaque period

       )
       transactions_expense = (
           transactions_expense
           .values('category')  # ça fait le "GROUP BY period"
           .annotate(total=Sum('amount'))  # somme les montants pour chaque period

       )
       labels = [t['period'] for t in transactions]
       data = [float(t['total']) for t in transactions]
       labels_income = [t['category'] for t in transactions_income]
       data_income = [float(t['total']) for t in transactions_income]
       labels_expense = [t['category'] for t in transactions_expense]
       data_expense = [float(t['total']) for t in transactions_expense]

       return JsonResponse({"label":labels,"data":data,"labels_income":labels_income,"data_income":data_income,"labels_expense":labels_expense,"data_expense":data_expense}, safe=False)

    form = TransactionDateRangeForm()
    return render(request,"lookfinanz/dashboard.html",{"form":form})
