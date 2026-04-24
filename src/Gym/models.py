from django.db import models

import datetime

from datetime import timedelta

from django.utils import timezone

from django.db.models import Count

# Create your models here.

class MainModel(models.Model) : # abstract model => database level مش ال python level وظيفته كلها ان باقي الموديلز تورث منه وبينشا بس علي
    
    created_at = models.DateTimeField(auto_now_add= True) # for creation date

    updated_at =  models.DateTimeField(auto_now= True) # for last modify date

    class Meta :

        abstract = True # حتخليه ميظهرش علي الداتا بيز ليفل فقط البايثون ليفل

class GymClassQuerySet(models.QuerySet) :

    def trending(self) :
        
        return self.annotate(members_count=Count('members')).filter(members_count__gt = 15)

class GymClassManager(models.Manager) :

    def get_queryset(self):

        return GymClassQuerySet(model = self.model , using= self.db)
    
    def trending(self) :
        
        return self.get_queryset().trending()

class GymClass(MainModel) :

    objects = GymClassManager()

    title = models.CharField(max_length=100)

    base_price = models.FloatField()

    start_date = models.DateTimeField()

    trainer = models.ForeignKey("Trainer" , on_delete= models.CASCADE , related_name= "GymClass_Trainer")

    members = models.ManyToManyField("Member" , related_name= "GymClass_Member")

    def __str__(self):
        
        return self.title
    
    def discount(self) :

        if self.start_date > (timezone.now() + timedelta(days=30)) : # USE_TZ=True المظبوطة علي settings عشان ميضربش ايرور بسبب الtimezone.now() method عشان يجيب الوقت الحالي لكن بيستعمل datetime.datetime.now() method مش بيستعمل ال django عنها وعرفت ان search وكنت عامل django time zones عن django حضرتك كنت اتكلمت ف اول سيشن ل
                                                                        # link => https://docs.djangoproject.com/en/6.0/topics/i18n/timezones/

            self.base_price *= 0.8
            
            return self.base_price
        
        return self.base_price
    
    class Meta :

        verbose_name_plural = "Gym Classes"

class Specialization(MainModel) :

    name = models.CharField(max_length= 100)

    def __str__(self):
        
        return self.name

class Trainer(MainModel) :

    name = models.CharField(max_length= 100)
    
    specialization = models.ForeignKey(Specialization , on_delete= models.CASCADE , related_name= "Trainer_Specialization")

    def __str__(self):
        
        return self.name

class Member(MainModel) :

    name = models.CharField(max_length= 100)

    balance = models.FloatField()

    def __str__(self):
        
        return self.name
    
    @property
    def is_vip(self) :

        return self.balance > 1000

class Branch(MainModel) :

    name = models.CharField(max_length= 100 , unique= True)

    location = models.CharField(max_length= 200 , unique= True)

    def __str__(self):
        
        return self.name

    class Meta :

        verbose_name_plural = "Branches"

class Equipment(MainModel) :

    name = models.CharField(max_length= 100)

    is_damaged = models.BooleanField(default= False)

    branch = models.ForeignKey(Branch , on_delete= models.CASCADE , related_name="Equipment_Branch")

    def __str__(self):
        
        return self.name
    
class damaged_EquipmentManager(models.Manager) : # link => https://docs.djangoproject.com/en/6.0/topics/db/managers/

    def get_queryset(self):

        return super().get_queryset().filter(is_damaged = True)

class damaged_Equipment(Equipment) :

    objects = damaged_EquipmentManager()

    class Meta :

        proxy = True

        verbose_name_plural = "Damaged Equipments"



