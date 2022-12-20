# 데이터가 올바르게 들어갔는지 검증할 떄 사용할 파일
from django import forms # 장고에서 forms 불러오기
from pybo.models import Question, Answer, Comment # ~/pytho/models 에서 Question 불러오기

## 데이터 파라미터(전달 받을 데이터, 여기전 subject와 contnet) 형식이 알맞게 들어왔는지 검증
## ModelForm은 테이블과 연동함과 동시에 데이터는 저장
class QuestionForm(forms.ModelForm):
    ## Meta 클래스를 지정해주는 것은 하나의 약속(반드시 필요)
    class Meta:
        ## 연동시킬 테이블을 model에 정의
        model = Question  # 사용할 모델을 Question과 연동
        ## Question 테이블에서 subject, content 컬럼을 사용하여 연동
        fields = ['subject', 'content'] # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
        }
        # 부트스트랩을 이용한 디자인 바꾸기
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용',
        }