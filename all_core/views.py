from django.shortcuts import render
from datetime import date as amazing_date
from datetime import timedelta
from .models import TotalModel, RoutineTotalModel
from .models import RoutineModel, DetailsModel
from json import dumps
from django.http import JsonResponse
import json
# Create your views here.


def home_view(request):
    today = amazing_date.today()
    dates_list = []
    for i in range(6):
        past_date = today - timedelta(days=i)
        if len(list(TotalModel.objects.filter(date = past_date))) == 0:
            dates_list.append(past_date)
        
    detail_list = DetailsModel.objects.all()
    details_len = len(detail_list)
    detail_text = detail_list[details_len-1].detail_text
    
    print(dates_list)
    return render(request, 'home.html', context={
        'dates' : dates_list,
        'detail_text': detail_text,
    })


def day_report_view(request, date):
    d = date.split(' - ')
    months_list = ['zero', 'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']

    day = int(d[1])
    month = int(months_list.index(d[0]))
    year = int(d[2])
    p_date = amazing_date(year, month, day)
    print(p_date)
    routine_objs_list = RoutineTotalModel.objects.filter(date = p_date)
    if not len(routine_objs_list)==0:
        routine_report = routine_objs_list
        total_report = TotalModel.objects.filter(date = p_date)[0]
        context = {
        'routine_report' : routine_report,
        'total_report'  : total_report
        }
    else:
        error = "Yes"
        context = {
            "error" : error,
        }


    return render(request, 'dayreport.html',context)


def report_input_view(request, day, month, year):

    int_day = int(day)
    int_month = int(month)
    int_year = int(year)
    print(int_day, int_month, int_year)
    return render(request, 'report_input.html', context = {
        "day": int_day,
        "month": int_month, 
        "year": int_year,
        })

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def report_questions_ajax(request):
    if request.method == 'POST' and is_ajax(request):
        print("here in ajax view")
        day = request.POST['day']
        month = request.POST['month']
        year = request.POST['year']
        print(day, month, year)
        all_routines = RoutineModel.objects.all()
        routines = []
        for routine in all_routines:
            all_tasks = routine.taskmodel_set.all()
            for task in all_tasks:
                new_list = [routine.number, task.code, task.name]
                routines.append(new_list)         

        data = routines
        data = dumps(data)
        return JsonResponse(data, safe=False)
    return 1

def report_input_ajax(request):
    if request.method == 'POST' and is_ajax(request):
        input_date = json.loads(request.POST['date'])
        data = json.loads(request.POST['parsed'])
        comment = json.loads(request.POST['comment'])
        year = int(input_date[0])
        month = int(input_date[1])
        day = int(input_date[2])
        date = amazing_date(year, month, day)
        
        print("commenyt", comment)
            
        
        routines = RoutineModel.objects.all()
        for routine in routines:
            routine_number = routine.number
            routine_list = []
            routine_marks = 0
            routine_total = 0
            tasks = []
            for ans in data:
                if ans[0] == routine_number:
                    routine_list.append(ans)
                    if ans[3] == "yes":
                        routine_marks+=2
                        routine_total+=2
                        tasks.append(1)
                        print("yes")
                    else:
                        routine_total+=2
                        tasks.append(0)         

            routine_obj=RoutineTotalModel(date = date, 
                                          routine = routine, 
                                          rtotal = routine_marks,
                                          total_marks = routine_total,
                                          tasks = tasks)
            routine_obj.save()

        total_obj = TotalModel(date = date, comment=comment)
        total_obj.save()

        some_data = []
        return JsonResponse(some_data, safe=False)
    return 1


month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}
month_numbers = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

def graph_view(request):
    routines_list = RoutineModel.objects.all()
    routines = [routine.number for routine in routines_list]
    routines = ["Total"] + routines
    total_list = TotalModel.objects.all()
    months_list = list(set([total.date.month for total in total_list]))
    months = [month_names[month] for month in months_list]
    years = list(set([total.date.year for total in total_list]))

    print(routines, months, years)


    return render(request, 'graph.html', context={
        "routines" : routines,
        "months"   : months,
        "years" :   years,
    })

def graph_ajax(request):
    if request.method == 'POST' and is_ajax(request):
        input_data = json.loads(request.POST['input'])
        year = int(input_data[0])
        month_name = input_data[1]
        month = int(month_numbers[month_name])
        routine = input_data[2]

        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from io import BytesIO
        import base64
        
        if routine == 'Total':
            total_graph_objs = TotalModel.objects.filter(date__year = year, date__month = month)
            
            total_marks = [obj.total for obj in total_graph_objs]
            total_pass_marks = [obj.pass_border for obj in total_graph_objs]
            total_days = [obj.date.day for obj in total_graph_objs]
            print("totalmarks", total_marks)
            print("totalpassmarks", total_pass_marks)
            print("totaldays", total_days)

            

            plt.bar(total_days, total_marks)
            plt.plot(total_days, total_pass_marks, color='red')
            plt.xlabel("Dates")
            plt.ylabel("Marks")
            plt.title(f"{month_name} - Total Marks Graph")
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=300)
            plt.close()

            image = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
            
            data = json.dumps({"img": image})

            return JsonResponse(data, safe=False)
        
        else:
            the_routine = RoutineModel.objects.get(number=routine)

            total_routine_objs = RoutineTotalModel.objects.filter(routine=the_routine, date__month=month)
            rtotal_marks = [obj.rtotal for obj in total_routine_objs]
            total_marks_list = [obj.total_marks for obj in total_routine_objs]
            total_days = [obj.date.day for obj in total_routine_objs]

            plt.bar(total_days, rtotal_marks)
            plt.plot(total_days, total_marks_list, color='red')
            plt.xlabel("Dates")
            plt.ylabel("Marks")
            plt.title(f"{month_name} - Routine {routine} Marks Graph")
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=300)
            plt.close()

            image = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
            
            data = json.dumps({"img": image})

            return JsonResponse(data, safe=False)




    return 1