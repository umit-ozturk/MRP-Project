from django.contrib.auth.models import BaseUserManager


class AmbarUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('The given username must be set')

        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None):
        return self._create_user(email, password, False, False)

    def create_superuser(self, email=None, password=None):
        return self._create_user(email, password, True, True)