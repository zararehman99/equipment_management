from django.db import models
from django.utils import timezone

from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from datetime import datetime, timedelta

from .models import Accounts, Roles, EquipmentDetails, Reservations, EquipmentReservations, EquipmentInventory, EquipmentCategory, ReservationStatus

from .forms import UserRegistrationForm, LoginForm, ReservationForm

from django.http import HttpResponseNotAllowed


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def index(request):
    context = {
        'name_model': 1,
        'num_equipment': 2,
        'num_equipment_available': 3,
        'num_categories': 4,
    }

    
    return render(request, 'index.html', context=context)



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Custom authentication logic
        user = authenticate_user(username, password)
        
        if user:
            # If user exists, create session and redirect
            request.session['user_id'] = user.ACCOUNT_ID
            if user.ROLE_ID.ROLE_TYPE == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('index')
        else:
            # If authentication fails, display error message
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')
    
def authenticate_user(username, password):
    # Custom authentication logic
    try:
        user = Accounts.objects.select_related('ROLE_ID').get(USER_NAME=username, PASSWORD=password)
        return user
    except Accounts.DoesNotExist:
        return None

def logout_view(request):
    # Delete user session to log out
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')

def inventory_view(request):
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', None)
    sort_by = request.GET.get('sort_by', None)
    sort_order = request.GET.get('sort_order', 'asc') 
    items_per_page = request.GET.get('items_per_page', 10)
    # Fetch all inventory items with category and available items left
    inventory_items = EquipmentInventory.objects.select_related('ID__CATEGORY_ID').annotate(
        id=models.F('ID__ID'),
        name=models.F('ID__NAME'),
        available_items=models.F('AVAILABLE'),
        lent_items=models.F('LENT'),
        onsite=models.F('ID__IS_ONSITE_ONLY'),
        warranty=models.F('ID__WARRANTY_YEARS'),
        description=models.F('ID__DESCRIPTION'),
        category_name=models.F('ID__CATEGORY_ID__CATEGORY_NAME')
    )
    if search_query:
        inventory_items = inventory_items.filter(
            # models.Q(ID__unaccent__icontains=search_query) |
            models.Q(ID__NAME__icontains=search_query) |  # Search name field
            models.Q(description__icontains=search_query)  # Search description field
        )
    # Apply category filter if provided
    if category_filter:
        inventory_items = inventory_items.filter(ID__CATEGORY_ID=category_filter)

    # Sort by available items if sort_by parameter is provided
    if sort_by:
        if sort_order == 'asc':
            inventory_items = inventory_items.order_by(sort_by)
        elif sort_order == 'desc':
            inventory_items = inventory_items.order_by(f'-{sort_by}')
    
    # Pagination
    paginator = Paginator(inventory_items, items_per_page)
    page = request.GET.get('page')
    try:
        inventory_items = paginator.page(page)
    except PageNotAnInteger:
        inventory_items = paginator.page(1)
    except EmptyPage:
        inventory_items = paginator.page(paginator.num_pages)

    context = {
        'inventory_items': inventory_items,
        'categories': EquipmentCategory.objects.all(),  # Pass all categories for filtering
        'selected_category': category_filter,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'search_query': search_query,
    }
    return render(request, 'inventory.html', context=context)

def add_to_reservation(request, equipment_id):
    try:
        equipment = EquipmentDetails.objects.get(pk=equipment_id)
        current_user_id = request.session.get('user_id')
        if not current_user_id:
            raise Exception("User not logged in")
        accounts = Accounts.objects.get(ACCOUNT_ID=current_user_id)
        inventory_item = EquipmentInventory.objects.filter(ID_id=equipment_id).first()

        if inventory_item and inventory_item.AVAILABLE <= 0:
            return JsonResponse({'success': False, 'text': "No such items left in inventory"})

        if inventory_item and equipment.IS_ONSITE_ONLY:
            reservation_type = 'Onsite'
        else:
            reservation_type = 'Borrow'
        
        # Check for pending reservations for the current user
        pending_reservations = Reservations.objects.filter(
            USER_ID=current_user_id,
            reservationstatus__STATUS='pending'
        ).select_related('USER_ID', 'reservationstatus')
        if pending_reservations.exists():
            # Add new items to the existing reservation
            existing_pending_reservation = pending_reservations.first()
            reservation = existing_pending_reservation
        else:
            # Create a new reservation with the current user's account
            reservation = Reservations.objects.create(USER_ID=accounts, CREATED_DATETIME=timezone.now(), UPDATED_DATETIME=timezone.now())
            # Mark the new reservation as pending
            ReservationStatus.objects.create(
                RESERVATION_ID=reservation,
                STATUS='pending'
            )
        # Ensure that the reservation object is created successfully
        if not reservation:
            raise Exception("Failed to create reservation")
        
        # Ensure that the reservation object is indeed an instance of Reservations
        if not isinstance(reservation, Reservations):
            raise Exception("Reservation object is not an instance of Reservations")
        # Create a new equipment reservation
        EquipmentReservations.objects.create(
            EQUIPMENT_ID=equipment, 
            RESERVATION_ID=reservation, 
            BORROW_DATE=timezone.now(), 
            RETURN_DATE=timezone.now() + timedelta(days=5), 
            PURPOSE='Reservation', 
            RESERVATION_TYPE=reservation_type
        )
        # Update the EquipmentInventory
        if inventory_item:
            inventory_item.LENT += 1
            inventory_item.AVAILABLE -= 1
            inventory_item.save()
        return JsonResponse({'success': True, 'text': 'Item added successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def view_reservations(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    reservations = Reservations.objects.filter(USER_ID=user_id).select_related('reservationstatus')
    
    context = {
        'reservations': reservations
    }
    return render(request, 'view_reservations.html', context=context)




def remove_reservation(request, reservation_id):
    try:
        reservation = EquipmentReservations.objects.get(pk=reservation_id)
        equipment_id = reservation.EQUIPMENT_ID_id
        reservation.delete()
        inventory_item = EquipmentInventory.objects.filter(ID_id=equipment_id).first()
        if inventory_item:
            inventory_item.LENT -= 1
            inventory_item.AVAILABLE += 1
            inventory_item.save()
        return JsonResponse({'success': True})
    except EquipmentReservations.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reservation not found'})

