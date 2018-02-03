from django.contrib import admin
from Geeker.models import User, Ticket, TicketRequest
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin, Group

# Register your models here.

class ProfileAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'first_name', 'last_name')}),
        ('Professional info', {'fields': ('field', 'info', 'website', 'image')}),
        ('Permissions', {'fields': ('is_admin', 'is_supplier')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, ProfileAdmin)
admin.site.register(Ticket)
admin.site.register(TicketRequest)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)