from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('Введите номер телефона')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.save()
        return user

    def create_superuser(self, phone_number):
        user = self.create_user(phone_number=phone_number)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
