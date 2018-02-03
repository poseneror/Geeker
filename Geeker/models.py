from django.db import models
import uuid
from Itay import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

FIELDS_CHOICES = (
    ('SE', 'Software Engineer'),
    ('EE', 'Electrical Engineer'),
    ('HE', 'Hardware Expert'),
    ('NE', 'Network Expert'),
)

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, db_index=True, unique=True)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="profile_pictures", blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    phone = PhoneNumberField(blank=True)
    website = models.URLField(blank=True, help_text="ex: http://www.yoursite.com")

    field = models.CharField(max_length=2, choices=FIELDS_CHOICES, blank=True)
    info = models.TextField(blank=True)

    available = models.BooleanField(default=False)
    response = models.IntegerField(null=True, blank=True)
    freelancers = models.ManyToManyField("self")

    is_supplier = models.BooleanField(default=False, verbose_name='supplier')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_rating(self):
        avg = 0
        count = 0
        tickets = Ticket.objects.filter(assigned=self).filter(reviewed=True)
        for rev in tickets:
            avg += rev.review_rating
            count += 1
        if count > 0:
            return "%.1f" % (avg / count)
        else:
            return False

    def get_pending(self):
        return TicketRequest.objects.filter(assigned=self).count()

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __unicode__(self):
        return self.get_full_name()


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="supplier", blank=True, null=True)
    assigned = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="expert", blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = PhoneNumberField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    solved = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    review_text = models.TextField(blank=True)
    review_rating = models.IntegerField(blank=True, null=True)

    def get_status(self):
        status = "waiting for a provider"
        if(self.supplier):
            status = "waiting for expert confirmation"
            if(self.assigned):
                status = "ticket pending"
                if(self.solved):
                    status = "ticket solved"
                    if(self.reviewed):
                        status = "solved and reviewed"
        return status


class TicketRequest(models.Model):
    ticket = models.OneToOneField(Ticket, related_query_name="ticketrequest")
    assigned = models.ForeignKey(settings.AUTH_USER_MODEL)
    time_created = models.DateTimeField(auto_now_add=True)


class EmploymentRequest(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="provider")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="it_expert")