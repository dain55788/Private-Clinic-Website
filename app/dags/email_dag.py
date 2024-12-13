# Test Sending Email with Twilio Sengrid
import ssl
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG


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
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True

# default arguments of a DAG
default_args = {
    'owner' : 'DainyNgyn',
    'depends_on_past':False,
    'start_date': datetime(2024, 12, 13),
    'email': ['dain55788@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries':'1',
    'retry_delay':timedelta(seconds=5),
    'catchup_by_default':False
}


# Define a DAG
email_dag = DAG(
    'Arrangement_Email',
    description='Automatically sending arrangement announcement email to patient ',
    default_args=default_args,
    schedule_interval='@once',  # run once
    tags=['arrangement_email_sengrid'],
    catchup=False,
)

# Define tasks phase
email_sender = PythonOperator(
    task_id='Arrangement_Email',
    python_callable=email,
    dag=email_dag
)
# DAG task dependencies:
email_sender