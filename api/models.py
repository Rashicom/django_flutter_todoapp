from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser, AbstractBaseUser


# custom user email based varification
class CustomUserManager(BaseUserManager):

    # overriding user based authentication methord to email base authentiction
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given mail must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)




# extrafields are added to by inheriting the django Abstract user
class CustomUser(AbstractUser):
    
    username = None

    # extra fields
    email = models.EmailField(primary_key=True)
    contact_number = models.CharField(max_length=12)
    user_otp = models.CharField(max_length=10,null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


# task model
class tasks(models.Model):
    email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task_id = models.AutoField(primary_key=True)
    task = models.CharField(max_length=50)
    task_details = models.TextField()
    task_initial_date = models.DateField(auto_now=False, auto_now_add=True)
    task_initial_time = models.TimeField(auto_now=False, auto_now_add=True)
    task_due_date = models.DateField(auto_now=False, auto_now_add=False)
    task_due_time = models.TimeField(auto_now=False, auto_now_add=False)
    task_status = models.BooleanField(default=False)


# {"task" :  "new task", "task_details" : "task_details new", "task_due_date": "26-06-2023", "task_due_time":"09:10"}
# {"email" : "", "contact_number" : "", "first_name" : ""  }
# Create your models here.