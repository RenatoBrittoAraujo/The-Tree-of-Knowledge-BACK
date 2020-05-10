from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    username = models.CharField(_('user name'), max_length=40, blank=False, null=False)
    bio = models.CharField(_('user bio'), max_length=200, blank=True, null=True)
    contributionpoints = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(User, self).save(*args, **kwargs)
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def report(self, reporter):
        if not reporter:
            return False
        if UserReport.objects.filter(reportee=self, reporter=reporter).exists():
            return False
        UserReport(reporter=reporter, reportee=self).save()
        return True
    
    def add_contribution(self, contribution_text):
        Contributions(text=contribution_text, user=self).save()

    def add_contribution_points(self, points):
        self.contributionpoints = self.contributionpoints + int(points)
        self.save()

class Contributions(models.Model):
    text = models.CharField(null=False, blank=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')

class UserReport(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_reported')
    reportee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reports')
