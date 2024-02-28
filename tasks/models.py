from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Plan(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='plans',
    )
    

    class Meta:
        verbose_name = _("plan")
        verbose_name_plural = _("plans")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plan_detail", kwargs={"pk": self.pk})

class Task(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    description = models.TextField(_("description"), blank=True, max_length=10000)
    project = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE, 
        verbose_name=_("project"), 
        related_name='tasks',
    )
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='tasks',
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    is_done = models.BooleanField(_("is done"), default=False, db_index=True)
    deadline = models.DateTimeField(_("deadline"), null=True, blank=True, db_index=True)
  

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        ordering = ['is_done', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})
