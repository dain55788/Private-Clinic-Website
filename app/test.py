from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from app import db
from app.src.models import Arrangement


# Overall steps for sending patient arrangement email
# 1. Retrieve the arrangement info in valid range of time (6p.m)
# 2. Check the phone of the arrangement with user's phone
# 3. Send email with from, to parameters


def email():
    # ssl._create_default_https_context = ssl._create_unverified_context
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
    import base64
    message = Mail(
        from_email='dainnguyen1307@gmail.com',
        to_emails='dain55788@gmail.com',
        subject='Nhắc nhở lịch khám',
        html_content='<img src="https://i.kym-cdn.com/entries/icons/original/000/048/241/tai_lung_computer_meme.jpg"> '
                     '<h1> Nhắc nhở lịch khám </h1>'
                     '<br>Lets go bruhhhh, successfully sending email<br>Thank you!'
    )

    # main execution
    sg = SendGridAPIClient("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")
    # your actual Sendgrid API key here
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


def get_valid_arrangements():
    """
    Retrieve arrangements where appointment_date is between:
    - 6 PM today
    - 6 PM tomorrow
    """
    # Step 1: Define the datetime range
    now = datetime.now()

    # Start range: 6 PM today
    start_of_range = datetime.combine(now.date(), time(18, 0, 0))  # 6 PM today

    # End range: 6 PM tomorrow
    end_of_range = start_of_range + timedelta(days=1)  # Add 24 hours for 6 PM next day

    print(f"Retrieving arrangements between {start_of_range} and {end_of_range}")

    # Step 2: Query the database for valid arrangements
    with Session(db.engine) as session:
        valid_arrangements = session.query(Arrangement).filter(
            Arrangement.appointment_date >= start_of_range,
            Arrangement.appointment_date < end_of_range
        ).all()

    # Step 3: Return the valid arrangements
    return valid_arrangements


# Main execution (check valid datetime to send email)

email()