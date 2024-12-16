from datetime import datetime, timedelta
from sqlalchemy import Date
from sqlalchemy.orm import Session
from app import db
from app.src.models import Arrangement
from app.src.models import User
from sqlalchemy import func
import json

# Overall steps for sending patient arrangement email
# 1. Retrieve the arrangement info in valid range of date
# 2. Check the phone of the arrangement with user's phone
# 3. Send email with from, to parameters


# return list of valid arrangements
def get_valid_arrangements():  # compare using the appointment_date information
    # Get today's date and the next day's date
    today = datetime.now().date()
    next_day = today + timedelta(days=1)
    next_day = str(next_day)
    # Query to get all arrangements that are scheduled for the next day
    arrangements = Arrangement.query.all()
    valid_arrangements = []
    for arr in arrangements:
        arr.appointment_date = str(arr.appointment_date)
        if arr.appointment_date.__eq__(next_day):
            valid_arrangements.append(arr)
    return valid_arrangements


def save_arrangements_to_json():
    valid_arrangements = get_valid_arrangements()
    print(len(valid_arrangements))
    for arr in valid_arrangements:
        print(arr.appointment_date)
        print(arr.patient_name)
        print(arr.phone)
    # Prepare the data to be written to JSON
    arrangements_data = {
        "sum_number_of_arrangements": len(valid_arrangements),
        "arrangements": []
    }

    # Extract relevant details from each arrangement
    for arr in valid_arrangements:
        arrangements_data["arrangements"].append({
            "email": arr.email,
            "patient_name": arr.patient_name,
            "phone": arr.phone,
            "appointment_date": arr.appointment_date
        })

    # Write data to a JSON file
    output_file = "data/arrangements.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(arrangements_data, file, indent=4, ensure_ascii=False)


# Main execution (check valid datetime to send email)
def email(arr: Arrangement, to_mail):
    # ssl._create_default_https_context = ssl._create_unverified_context
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
    import base64
    message = Mail(
        from_email='dainnguyen1307@gmail.com',
        to_emails=to_mail,
        subject='Nhắc Nhở Lịch Khám',
        html_content='<img src="https://static.vecteezy.com/system/resources/previews/019/956/427/non_2x/healthy-food-logo-premium-vector.jpg"'
                     'style="width:300px; height:auto;">'
                     '<h1> Nhắc nhở lịch khám </h1>'
                     f'<br>Email bệnh nhân đăng ký: {arr.email}<br>'
                     f'<br>Tên bệnh nhân: {arr.patient_name}<br>'
                     f'<br>Số điện thoại: {arr.phone}<br>'
                     f'<br>Ngày khám: {arr.appointment_date}<br>'
                     f'<br>Địa chỉ: 97 Võ Văn Tần, Quận 3, Thành phố Hồ Chí Minh<br>'
                     f'<br style="font-color: red">Ghi chú: Nhớ mang theo CĂN CƯỚC CÔNG DÂN và BẢO HIỂM Y TẾ bạn nhé!!<br>'
    )

    # main execution
    sg = SendGridAPIClient("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")
    # your actual Sendgrid API key here
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


save_arrangements_to_json()
valid_arrangements = get_valid_arrangements()
for arr in valid_arrangements:
    email(arr, arr.email)
