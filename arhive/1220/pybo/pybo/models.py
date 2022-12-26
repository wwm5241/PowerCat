from django.db import models
from django.contrib.auth.models import User

# 질문 테이블 정의
class Question(models.Model):
    # author 속성 추가 - 모델을 변경한 후에는 반드시 makemigrations와 migrate를 통해 데이터베이스를 변경
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    # models 클래스의 CharField() 함수를 이용해여 컬럼 정의
    # html에서의 varchar(200)과 같은 의미로 만들기
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    # 추천인 기능 추가
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject

# 답변 테이블 정의
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    # 테이블끼리 연동시키기 위해 외래키 지정
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ForeignKey는 다른 모델과 연결하기 위해 사용
    # on_delete=models.CASCADE의 의미는 이 답변과 연결된 질문(Question)이 삭제될 경우 답변(Answer)도 함께 삭제된다는 의미
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

# 댓글 테이블 정의
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)