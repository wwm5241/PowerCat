from .models import Answer
from datetime import datetime, timedelta


def delete_answer():
    
    records = Answer.objects.all()
    
    for a in records:
        if a.checking=='O':
            a.checking='X'
            print(a.author, a.question, a.content ,a.create_date)
            a.save()
    
    

