from django.db import models
from django.core.validators import MinValueValidator

class Group(models.Model):
	uid = models.CharField(primary_key=True, max_length=8)
	registered = models.DateTimeField(auto_now_add=True)

class User(models.Model):
	uid = models.CharField(primary_key=True, max_length=28)
	first_name = models.CharField(max_length=20, blank=False)
	last_name = models.CharField(max_length=20, blank=False)
	phone = models.PositiveIntegerField(max_length=10, blank=False)
	registered = models.DateTimeField(auto_now_add=True)
	group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

class Laundry(models.Model):
	start_time = models.DateTimeField(blank=False)
	end_time = models.DateTimeField(blank=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Payment(models.Model):
	creditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_creditor')
	debtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_debtor')
	amount = models.FloatField(blank = False)
	time_due = models.DateTimeField()
	paid = models.BooleanField(blank = False)

class Shower(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	start_time = models.DateTimeField(blank=False)
	end_time = models.DateTimeField(blank=False)

class Guests(models.Model):
	needs_privacy = models.BooleanField(blank = False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	start_time = models.DateTimeField(blank=False)
	end_time = models.DateTimeField(blank=False)
	num_guests = models.IntegerField(blank = False, validators=[MinValueValidator(1)])

class Plan(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	start_time = models.DateTimeField(blank=False)
	end_time = models.DateTimeField(blank=False)
	notes = models.CharField(max_length=500)

class Chore(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	notes = models.CharField(max_length=250)
	time_due = models.DateTimeField(blank=False)

class PostIt(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	notes = models.CharField(max_length=250)
	closed = models.BooleanField(blank = False)