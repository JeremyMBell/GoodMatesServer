from django.db import models
from django.core.validators import MinValueValidator

class Group(models.Model):
	id = models.AutoField(primary_key=True)

class User(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=20, blank=False)
	last_name = models.CharField(max_length=20, blank=False)
	registered = models.DateField(auto_now_add=True)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Roommates(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE)
	user2 = models.ForeignKey(User, on_delete=models.CASCADE)

class Laundry(models.Model):
	start_time = models.DateField(blank=False)
	end_time = models.DateField(blank=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Payment(models.Model):
	creditor = models.OneToOneField(User, on_delete=models.CASCADE)
	debtor = models.OneToOneField(User, on_delete=models.CASCADE)
	amount = models.FloatField(blank = False)
	time_due = models.DateField()
	paid = models.BooleanField(blank = False)

class Shower(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	start_time = models.DateField(blank=False)
	end_time = models.DateField(blank=False)

class Guests(models.Model):
	sock_on_door = models.BooleanField(blank = False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	start_time = models.DateField(blank=False)
	end_time = models.DateField(blank=False)
	num_guests = models.IntegerField(blank = False, validators=[MinValueValidator(1)])

class Plan(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	start_time = models.DateField(blank=False)
	end_time = models.DateField(blank=False)
	notes = models.CharField(max_length=500)

class Chore(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	notes = models.CharField(max_length=250)
	due = models.DateField(blank=False)

class PostIt(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	notes = models.CharField(max_length=250)
	closed = models.BooleanField(blank = False)