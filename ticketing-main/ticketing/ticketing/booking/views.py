import profile
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
import json

from .forms import RechargeForm, YourProfileForm
from .models import UserProfile, Recharge, Ticket
from datetime import date
# Temporary session variable (used for balance simulation)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

current_balance = 200


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        occupation = request.POST['occupation']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        # Create User
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Create UserProfile with extra data
        UserProfile.objects.create(
            user=user,
            mobile=mobile,
            gender=gender,
            occupation=occupation
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'booking/signup.html')

# ✅ LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'booking/login.html')

# ✅ LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')

# ------------------------
# HOMEPAGE VIEW
# ------------------------
# ✅ PROTECTED HOMEPAGE VIEW


@login_required
def homepage(request):
    # Example balance logic
    current_balance = 200

    # Get the last 2 recent tickets
    recent_tickets = Ticket.objects.filter(user=request.user).order_by('-timestamp')[:2]

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, 'booking/homepage.html', {
        'balance': current_balance,
        'recent_tickets': recent_tickets,
        'profile': profile,
    })



# ------------------------
# PURCHASING PAGE VIEW
# ------------------------
@login_required(login_url='login')
def purchasing_view(request):
    return render(request, 'booking/purchasing.html', {'balance': current_balance})

# ------------------------
# PROFILE VIEW (simplified, no login)
# ------------------------
@login_required(login_url='login')
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = YourProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = YourProfileForm(instance=profile)

    return render(request, 'booking/profile.html', {
        'profile': profile,
        'form': form
    })

# ------------------------
# RECHARGE VIEW
# ------------------------
def add_recharge(request):
    global current_balance
    if request.method == 'POST':
        form = RechargeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            current_balance += int(amount)  # Simulate balance update
            messages.success(request, f'Recharged ₹{amount} successfully.')
            return redirect('homepage')
    else:
        form = RechargeForm()

    return render(request, 'booking/add_recharge.html', {'form': form})

# ------------------------
# BALANCE API
# ------------------------
def get_balance(request):
    global current_balance
    return JsonResponse({"success": True, "balance": current_balance})

# ------------------------
# TICKET VIEW (HTML only)
# ------------------------

def ticket_view(request):
    today_date = date.today().strftime("%Y-%m-%d")
    # Also pass other data: from_station, to_station, etc.!
    context = {
        "from_station": request.session.get("from_station", ""),
        "to_station": request.session.get("to_station", ""),
        "date": request.session.get("ticket_date", ""),  # Or use today_date
        "today_date": today_date,
    }
    return render(request, "booking/ticket.html", context)

# ------------------------
# GUIDE VIEW (shows from/to stations)
# ------------------------
def guide_view(request):
    from_station = request.session.get('from_station', '-')
    to_station = request.session.get('to_station', '-')
    return render(request, 'booking/guide.html', {
        'balance': current_balance,
        'from_station': from_station,
        'to_station': to_station
    })

# ------------------------
# BUY TICKET LOGIC (deduct balance)
# ------------------------
@csrf_exempt
def buy_ticket(request):
    global current_balance
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fare = int(data.get("fare", 0))
            from_station = data.get("from", "-")
            to_station = data.get("to", "-")

            if current_balance >= fare:
                current_balance -= fare

                # Save trip details in session
                request.session['from_station'] = from_station
                request.session['to_station'] = to_station

                return JsonResponse({"success": True, "newBalance": current_balance})
            else:
                return JsonResponse({"success": False, "message": "Insufficient balance"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Only POST requests allowed"})
