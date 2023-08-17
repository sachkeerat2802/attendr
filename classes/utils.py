import io
import cv2
import base64
import xlsxwriter
import pytesseract
import numpy as np
from datetime import date
from pytesseract import Output
from .models import Attendance
from pyzbar.pyzbar import decode
from users.models import UserProfile


def detect_id(class_obj, lecture, data):
    image_base64 = data["video"]
    image_bytes = base64.b64decode(image_base64.split(",")[1])

    image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)

    for barcode in decode(image):
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        ocr = pytesseract.image_to_data(
            image, output_type=Output.DICT)
        ocr_data = ocr['text']
        words = ["Director's", "Signature"]

        if barcode_type == "CODE39":
            profile = UserProfile.objects.get(prn=barcode_data)
            if profile in class_obj.users.all():
                words.append(str(profile.prn))
                words.append(profile.name.split(" ")[0])

                if all(word in ocr_data for word in words):
                    instance = Attendance.objects.get(
                        lecture=lecture, profile=profile)

                    if instance.value != "P":
                        log = Attendance.objects.get(
                            profile=profile, lecture=lecture)
                        log.value = "P"
                        log.save()
                        return {'success': f'{profile.prn} : Present'}
                    else:
                        return {'info': f"Attendance for {profile.prn} already marked!"}
            else:
                return {'info': f"{profile.prn} is not a part of this class!"}
        else:
            return {'info': f"Invalid barcode type!"}


def generate_lecture_report(class_obj, lecture):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "S.No")
    worksheet.write(0, 1, "PRN")
    worksheet.write(0, 2, "Student Name")
    worksheet.write(
        0, 4, f"{str(lecture.start_time)[8:10]+'-'+str(lecture.start_time)[5:7]+'-'+str(lecture.start_time)[0:4]}  :  {str(lecture.start_time)[11:16]} - {str(lecture.end_time)[11:16]}")

    worksheet.set_column(1, 1, 15)
    worksheet.set_column(2, 2, 25)
    worksheet.set_column(4, 4, 22)

    logs = Attendance.objects.filter(class_object=class_obj, lecture=lecture)
    for i, log in enumerate(logs):
        worksheet.write(i + 1, 0, i + 1)
        worksheet.write(i + 1, 1, log.profile.prn)
        worksheet.write(i + 1, 2, log.profile.name)
        worksheet.write(i + 1, 4, log.value)

    workbook.close()
    output.seek(0)
    return output


def generate_class_report(class_obj, lectures):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "S.No")
    worksheet.write(0, 1, "PRN")
    worksheet.write(0, 2, "Student Name")
    worksheet.write(0, 4, "Percentage")
    worksheet.write(0, 5, "Present")
    worksheet.write(0, 6, "Absent")
    worksheet.write(0, 7, "Total")
    worksheet.set_column(0, 0, 5)
    worksheet.set_column(1, 1, 15)
    worksheet.set_column(2, 2, 25)
    worksheet.set_column(4, 4, 10)
    percentage_format = workbook.add_format({'num_format': '0.00%'})

    for i, lecture in enumerate(list(lectures)):
        worksheet.write(
            0, 9 + i, f"{str(lecture.start_time)[8:10]+'-'+str(lecture.start_time)[5:7]+'-'+str(lecture.start_time)[0:4]}  :  {str(lecture.start_time)[11:16]} - {str(lecture.end_time)[11:16]}")
        worksheet.set_column(9 + i, 9 + i, 22)

    users = class_obj.users.all()
    for i, user in enumerate(users):
        worksheet.write(i + 1, 0, i + 1)
        worksheet.write(i + 1, 1, user.prn)
        worksheet.write(i + 1, 2, user.name)

        user_total = Attendance.objects.filter(
            class_object=class_obj, profile=user)
        user_present = Attendance.objects.filter(
            class_object=class_obj, profile=user, value="P")

        worksheet.write(
            i + 1, 4, (len(user_present)/len(user_total)), percentage_format)
        worksheet.write(i + 1, 5, len(user_present))
        worksheet.write(i + 1, 6, len(user_total)-len(user_present))
        worksheet.write(i + 1, 7, len(user_total))

        for j, lecture in enumerate(list(lectures)):
            log = Attendance.objects.get(
                class_object=class_obj, lecture=lecture, profile=user)
            worksheet.write(i + 1, 9 + j, log.value)

    workbook.close()
    output.seek(0)
    return output
