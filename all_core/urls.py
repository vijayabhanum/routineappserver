from django.urls import path
from .views import home_view, day_report_view, report_input_view, graph_view
from .views import report_questions_ajax, report_input_ajax, graph_ajax
urlpatterns = [
    path("", home_view, name='home_page'),
    path("day_report/<date>", day_report_view, name='day_report_page'),
    path("input/<day>/<month>/<year>", report_input_view, name='report_input_page'),
    path("report_questions_ajax/", report_questions_ajax, name="questions_ajax"),
    path("report_input_ajax/",report_input_ajax, name="input_ajax"),
    path("graph",graph_view, name="graph_page"),
    path("graph_ajax/", graph_ajax, name="graph_ajax"),

]
