from django.contrib import admin

from .models import GymClass , Specialization , Trainer , Member , Branch , Equipment , damaged_Equipment

# Register your models here.

admin.site.register(GymClass)

admin.site.register(Specialization)

admin.site.register(Trainer)

admin.site.register(Member)

admin.site.register(Branch)

admin.site.register(Equipment)

class damaged_EquipmentAdmin(admin.ModelAdmin) : # stack overflow عرفتها من
                                                # link => https://stackoverflow.com/questions/23779250/using-proxy-model-in-django-admin-to-customize-change-list-view
                                                # admin.ModelAdmin => والكلاسيز طبعا اللي بتورث منه بدورها بتقوم بنفس المهمة admin panel ده كلاس مخصص للتحكم لطريقة عرض الداتا ع ال
    def get_queryset(self, request):
        return damaged_Equipment.objects.filter(is_damaged = True) # True يكون قيمته ب is_damaged بشرط ان عمود ال damaged_Equipment اللي من ال objects حترجع كل ال get_queryset ال

admin.site.register(damaged_Equipment , damaged_EquipmentAdmin) # damaged_EquipmentAdmin اللي جوا ال get_queryset method الداتا اللي فيه تتعرض زي ما انا محدد جوا ال admin panel يتفتح ف ال damaged_Equipment modelf بحيث لما ال  mapping ده اعتقد اشبه بال
                                                                # get_queryset => اللي حتتعرضلي هي اللي علي حسب الشرط اللي ف الفلتر بس objects فبكده حضمن دايما ان ال model دايما مع ال call  بيتعملها