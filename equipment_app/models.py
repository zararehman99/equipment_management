from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(InventoryItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# Create your models here.
class Addresses(models.Model):
    ID = models.AutoField(primary_key=True)  # Unique address identifier
    STREET = models.CharField(max_length=100)  # Street address
    CITY = models.CharField(max_length=100)  # City
    PROVINCE = models.CharField(max_length=100)  # Province
    POSTAL_CODE = models.CharField(max_length=10)  # Postal code

    class Meta:
        db_table = 'Addresses'
        unique_together = (('STREET', 'CITY', 'PROVINCE', 'POSTAL_CODE'),)

    def __str__(self):
        return f"Address: {self.STREET}"

class Roles(models.Model):
    ROLE_ID = models.AutoField(primary_key=True)  # Unique role identifier
    ROLE_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User')
    ]
    ROLE_TYPE = models.CharField(max_length=10, choices=ROLE_TYPE_CHOICES)  # Type of role, either admin or user

    class Meta:
        db_table = 'Roles'

    def __str__(self):
        return f"Role: {self.ROLE_TYPE}"

class Accounts(models.Model):
    ACCOUNT_ID = models.AutoField(primary_key=True)  # Unique account identifier
    FIRST_NAME = models.CharField(max_length=100)  # First name of the account holder
    LAST_NAME = models.CharField(max_length=100)  # Last name of the account holder
    USER_NAME = models.CharField(max_length=100, unique=True)  # Unique username for login
    BIRTHDATE = models.DateField()  # Date of birth of the account holder
    PHONE_NUMBER = models.CharField(max_length=20)  # Phone number of the account holder
    EMAIL = models.EmailField(unique=True)  # Email address of the account holder
    PASSWORD = models.CharField(max_length=100)  # Password for account login
    ADDRESS_ID = models.ForeignKey(Addresses, on_delete=models.CASCADE)  # ForeignKey for address reference
    ROLE_ID = models.ForeignKey(Roles, on_delete=models.CASCADE)  # ForeignKey for role reference

    class Meta:
        db_table = 'Accounts'

    def __str__(self):
        return f"Account userName: {self.USER_NAME}"

   
  

class UserSignupStatus(models.Model):
    USER_ID = models.OneToOneField(Accounts, primary_key=True, on_delete=models.CASCADE)  # Unique user identifier
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    STATUS = models.CharField(max_length=10, choices=STATUS_CHOICES)  # Status of user signup

    class Meta:
        db_table = 'UserSignupStatus'

    def __str__(self):
        return f"USER ID: {self.USER_ID} Status: {self.STATUS}"

class EquipmentCategory(models.Model):
    CATEGORY_ID = models.AutoField(primary_key=True)  # Unique category identifier
    CATEGORY_NAME = models.TextField()  # Name of the category

    class Meta:
        db_table = 'EquipmentCategory'

    def __str__(self):
        return f"CATEGORY_NAME: {self.CATEGORY_NAME}"

class EquipmentDetails(models.Model):
    ID = models.AutoField(primary_key=True)  # Unique equipment identifier
    CATEGORY_ID = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)  # Foreign key referencing equipment category
    NAME = models.CharField(max_length=100)  # Name of the equipment
    DESCRIPTION = models.TextField()  # Description of the equipment
    IS_ONSITE_ONLY = models.BooleanField()  # Flag indicating if equipment is onsite only
    WARRANTY_YEARS = models.IntegerField()  # Warranty duration in years

    class Meta:
        db_table = 'EquipmentDetails'

    def __str__(self):
        return f"NAME: {self.NAME}"

class EquipmentInventory(models.Model):
    ID = models.OneToOneField(EquipmentDetails, primary_key=True, on_delete=models.CASCADE)  # Unique inventory identifier, also referencing EquipmentDetails
    LENT = models.IntegerField()  # Number of equipment lent
    AVAILABLE = models.IntegerField()  # Number of equipment available

    class Meta:
        db_table = 'EquipmentInventory'

    def __str__(self):
        return f"ID: {self.ID}"

class Reservations(models.Model):
    RESERVATION_ID = models.AutoField(primary_key=True)  # Unique reservation identifier
    USER_ID = models.ForeignKey(Accounts, on_delete=models.CASCADE)  # Foreign key referencing users
    CREATED_DATETIME = models.DateTimeField(auto_now_add=True)  # Date of reservation creation
    UPDATED_DATETIME = models.DateTimeField()

    class Meta:
        db_table = 'Reservations'

    def __str__(self):
        return f"Reservation ID: {self.RESERVATION_ID}, User ID: {self.USER_ID}, Created Date: {self.CREATED_DATETIME}"

class EquipmentReservations(models.Model):
    ID = models.AutoField(primary_key=True)  # Unique reservation identifier
    EQUIPMENT_ID = models.ForeignKey(EquipmentDetails, on_delete=models.CASCADE)  # Foreign key referencing equipment details
    RESERVATION_ID = models.ForeignKey(Reservations, null=True, on_delete=models.CASCADE)  # Foreign key referencing reservations
    BORROW_DATE = models.DateField()  # Date of borrowing equipment
    RETURN_DATE = models.DateField()  # Date of returning equipment
    PURPOSE = models.TextField()  # Purpose of reservation
    RESERVATION_TYPE_CHOICES = [
        ('onsite', 'Onsite'),
        ('borrow', 'Borrow')
    ]
    RESERVATION_TYPE = models.CharField(max_length=10, choices=RESERVATION_TYPE_CHOICES)  # Type of reservation

    class Meta:
        db_table = 'EquipmentReservations'

    def __str__(self):
        return f"Reservation ID: {self.ID}, EQUIPMENT_ID: {self.EQUIPMENT_ID}, BORROW_DATE: {self.BORROW_DATE}"

class ReservationStatus(models.Model):
    RESERVATION_ID = models.OneToOneField(Reservations, primary_key=True, on_delete=models.CASCADE)  # Unique reservation identifier, also the primary key
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    STATUS = models.CharField(max_length=10, choices=STATUS_CHOICES)  # Status of reservation

    class Meta:
        db_table = 'ReservationStatus'

    def __str__(self):
        return f"Reservation ID: {self.RESERVATION_ID}, STATUS: {self.STATUS}"
