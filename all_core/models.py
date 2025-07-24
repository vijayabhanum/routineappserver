from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
Y_N_choice = [('Yes','Yes'), ('No', 'No')]
Codes = [
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
    ('e', 'e'),
    ('f', 'f'),
    ('g', 'g'),
    ('h', 'h'),
    ('i', 'i'),
    ('j', 'j')
]

class RoutineModel(models.Model):
    limited = models.CharField(max_length=5, choices=Y_N_choice, default='Yes')
    number = models.SmallIntegerField(
        validators= [MinValueValidator(1), MaxValueValidator(10)] )
    
    def __str__(self):
        return f"Routine {str(self.number)}"

class TaskModel(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=1, choices=Codes, default='a')
    routine = models.ForeignKey(RoutineModel, on_delete=models.CASCADE)

    def __str__(self):
        this_routine = self.routine.number
        return f"Routine {str(this_routine)} - Code ({self.code})"
    
    def clean(self):
        this_routine_limited = self.routine.limited
        if this_routine_limited == 'Yes':
            if self.code=='f' or self.code=='g' or self.code=='h'or self.code=='i' or self.code=='j':
                raise ValidationError("Limited Routine, cant add more than 5 tasks.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    

class RoutineTotalModel(models.Model):
    date = models.DateField(default=date.today)
    routine = models.ForeignKey(RoutineModel, on_delete=models.CASCADE)
    rtotal = models.SmallIntegerField(default=0)
    total_marks = models.SmallIntegerField(default=10)
    tasks = models.CharField(max_length=20, default= "example")

    def __str__(self):
        return f"{str(self.date)} - {self.routine} - tot:{self.rtotal}"
    
    def save(self, *args, **kwargs):
        if len(RoutineTotalModel.objects.filter(routine = self.routine, date = self.date)) == 0:
            super().save(*args, **kwargs)
        else:
            raise ValidationError("routine total for this date is already created !!!")



class TotalModel(models.Model):
    date = models.DateField(default=date.today)
    total = models.SmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    passorfail = models.BooleanField(default='False')
    pass_border = models.SmallIntegerField(default=40)
    comment = models.CharField(max_length=50, default="example")
    def __str__(self):
        return f"{str(self.date)} - Total {self.total}"
    
    def cal_total(self):
        this_date = self.date
        all_routines = RoutineTotalModel.objects.all().filter(date = this_date)
        this_total = 0
        for r in all_routines:
            this_total += r.rtotal
        self.total = this_total



    def save(self, *args, **kwargs):
        if len(TotalModel.objects.filter(date=self.date)) == 0:
            objs_list = PassMarksModel.objects.all()
            len_obj = len(objs_list)
            pass_obj = objs_list[len_obj-1]
            self.pass_border = pass_obj.pass_marks
            self.cal_total()
            if self.total > self.pass_border:
                self.passorfail = 'True'
            else:
                self.passorfail = 'False'
            if self.total > 100:
                self.total = 100

            super().save(*args, **kwargs)
        else:
            raise ValidationError("total for this date is already created !!!")

class PassMarksModel(models.Model):
    pass_marks = models.SmallIntegerField(default=40)


class DetailsModel(models.Model):
    detail_text = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        all_routines = RoutineModel.objects.all()
        text = ""
        text += f"Date: {self.date}" + "\n" + "\n"
        for routine in all_routines:
            text += f"Routine - {routine.number}" + "\n"
            tasks = routine.taskmodel_set.all()
            for task in tasks:
                text += f"--------- {task.code}. {task.name}" + "\n"
            text += "\n"
        self.detail_text = text
        super().save(*args, **kwargs)
    



