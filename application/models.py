from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
import os

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    skill = models.CharField(max_length=20)
    creation_date= models.DateTimeField(auto_now_add=True)
    features = models.CharField(max_length=200,blank=True, null=True)
    model = models.FileField(blank = True, null = True, upload_to="projects/model")
    dataset= models.FileField(blank = True, null = True, upload_to="projects/dataset")
    algorithm = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User,related_name='projects', on_delete=models.CASCADE)
    objects = models.Manager() 

    def __str__(self):
        return self.name

    def json_data(self):
        project={"d":self.pk, "target":self.target, "skill": self.skill}

        return project
    
@receiver(models.signals.pre_save, sender=Project)
def auto_delete_model_on_change(sender, instance,**kwargs):

        if not instance.pk:
            return False
        
        try:
            old_model = sender.objects.get(pk=instance.pk).model
        except sender.DoesNotExist:
            return False

        new__model = instance.model

        if not old_model == new__model:
            if os.path.isfile(old_model.path):
                os.remove(old_model.path)


@receiver(models.signals.pre_save, sender=Project)
def auto_delete_dataset_on_change(sender, instance,**kwargs):

        if not instance.pk:
            return False
        
        try:
            old_dataset = sender.objects.get(pk=instance.pk).dataset
        except sender.DoesNotExist:
            return False

        new_dataset = instance.dataset

        if not old_dataset == new_dataset:
            if os.path.isfile(old_dataset.path):
                os.remove(old_dataset.path)


class ProjectManager(models.Manager):
    pass
