from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class CV(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    other_achievements = models.TextField()
    skills_abilities = models.TextField()
    interests = models.TextField()
    public = models.BooleanField()

    def achievement_list(self):
        return self.other_achievements.split('\n')

    def skill_list(self):
        return self.skills_abilities.split('\n')

    def __str__(self):
        return self.owner.username

class Referee(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AddressReferee(models.Model):
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE)

    line_1 = models.CharField(max_length=50)
    line_2 = models.CharField(max_length=50, blank=True)
    town_city = models.CharField(max_length=20)
    post_code = models.CharField(max_length=8)

    def __str__(self):
        return self.line_1

class AddressCV(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)

    line_1 = models.CharField(max_length=50)
    line_2 = models.CharField(max_length=50, blank=True)
    town_city = models.CharField(max_length=20)
    post_code = models.CharField(max_length=8)

    def __str__(self):
        return self.line_1

class Education(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)

    location = models.CharField(max_length=75)
    comments = models.TextField()

    def __str__(self):
        return self.location

class TechSkill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.title

    def tech_skill_list(self):
        return self.text.split('\n')

class WorkExperience(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.title
