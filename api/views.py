import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from classes.models import Class
from base.models import TimeTable
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import StaffProfile, UserProfile


@api_view(['GET'])
def get_timetable(request, date):

    url = f"http://time-table.sicsr.ac.in/day.php?year={date[0:4]}&month={date[5:7]}&day={date[8:10]}"

    classes = []
    links = []
    subjects = []

    user = request.user
    timetable_objects = TimeTable.objects.filter(user=user)
    for obj in timetable_objects:
        subjects.append(obj.name)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    for link in soup.find_all('a'):
        for subject in subjects:
            if link.get('title') != None and subject in link.get('title'):
                str = "http://time-table.sicsr.ac.in/" + link.get('href')
                links.append(str)

    for link in links:
        req = requests.get(link)
        soup = BeautifulSoup(req.content, "html.parser")
        tags = soup.find_all('td')

        class_obj = {}

        for tag in tags:
            if tag.string == "Description:":
                rindex = tag.find_next_sibling().string.rfind("-")
                lindex = tag.find_next_sibling().string.rfind(":") + 1
                class_obj['name'] = tag.find_next_sibling(
                ).string[lindex:rindex]

            if tag.string == "Description:":
                lindex = tag.find_next_sibling().string.rfind("-") + 1
                class_obj['faculty'] = tag.find_next_sibling().string[lindex:]

            if tag.string == "Room:":
                class_obj['room'] = tag.find_next_sibling().string[-3:]

            if tag.string == "Start time:":
                class_obj['time'] = tag.find_next_sibling().string[:5] + " - "

            if tag.string == "End time:":
                class_obj['time'] += tag.find_next_sibling().string[:5]

        classes.append(class_obj)

    return Response(classes)


@api_view(['GET'])
def get_search(request, query):

    if query != "":
        result = {}

        result['users'] = list(UserProfile.objects.distinct().filter(
            Q(prn__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query)
        ).values())

        result['staff'] = list(StaffProfile.objects.distinct().filter(
            Q(empno__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query)
        ).values())

        result['classes'] = list(Class.objects.distinct().filter(
            Q(name__icontains=query)
        ).values())

        return JsonResponse(result)
