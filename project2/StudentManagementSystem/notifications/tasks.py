from students.models import Student
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_daily_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        if student.needs_attendance_reminder:
            send_mail(
                'Attendance Reminder',
                'Please mark your attendance for today.',
                'kdamir2004@gmail.com',
                [student.email],
                fail_silently=False,
            )

@shared_task
def notify_grade_update(student_id, course_name, grade):
    # Fetch the student based on ID
    student = Student.objects.get(pk=student_id)  # Assuming ID is used for lookup
    send_mail(
        'Grade Update Notification',
        f'Your grade in {course_name} has been updated to {grade}.',
        'kdamir2004@gmail.com',
        [student.email],
        fail_silently=False,
    )

@shared_task
def generate_daily_report():
    # Logic to generate a daily attendance and grade report
    send_mail(
        'Daily Report',
        'Here is the summary of attendances and grades.',
        'from@example.com',
        ['kdamir2004@gmail.com'],
        fail_silently=False,
    )

@shared_task
def send_weekly_performance_summary():
    students = Student.objects.all()  # Fetch all students or as necessary
    for student in students:
        send_mail(
            f'Weekly Performance Summary for {student.name}',
            'Here is your weekly performance summary.',
            'kdamir2004@gmail.com',
            [student.email],
            fail_silently=False,
        )
