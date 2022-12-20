from django.urls import path
# 실제 요청을 처리하기 위해 현재 디렉토리 내의 views.py 임포트
from . import views

## 해당 urls.py에도 별칭을 붙일 수 있음
## 타 프로젝트에서 pybo 프로젝트의 html을 사용할 수 있기 때문에 구별을 지어주는 것이 바람직함
app_name = 'pybo'

urlpatterns = [
    # 127.0.0.1/pybo/ 요청이 왔을 경우 views.index로 처리됨
    path('', views.index, name="index"),
    # 추가적인 요청에 대한 응답을 위해 경로를 추가
    # pybo/정수 요청이 왔을 경우 정수를 받아서 question_id에게 넘겨줌
    # 여기서 올 수 있는 자료형은 int, str, slug(ASCII, 숫자, 하이픈, 밑줄)
    # 경로를 표현할 때 정규표현식을 사용하여 좀 더 복잡하게 표현 가능(정규표현식: path가 아닌 -> re_path로 작성)
    ## 127.0.0.1:8000/pybo/1/ 아닌 별칭을 지정하면 다양한 방식으로 views.detail에 접근 가능하다
    path('<int:question_id>/', views.detail, name="detail"),# int(숫자)를 받아 questuon_id에 보내겠다는 의미
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    # 질문 댓글 등록, 수정, 삭제 URL 매핑
    path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),
    # 답변 댓글 등록, 수정, 삭제 URL 매핑
    path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'),
]
