# from django.http import HttpResponse
# html 파일로의 전달 역할을 하는 render
# 존재하지 않는 응답에 요청을 한 경우 404 not found 에러 처리
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .models import Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.
# 응답에 대한 처리 함수를 정의할 땐 무조건 매개변수 1개이상 필요
def index(request):
    # 날짜의 역순 = -create_date
    question_list = Question.objects.order_by('-subject')
    context = {'question_list':question_list}
    # templates 설정을 settings.py 파일에 등록 후
    # templates 폴더하위에 pybo 폴더 폴더를 생성하고 question_list.html 파일생성
    return render(request, 'pybo/question_list.html', context)

# urls.py에서 넘겨받은 숫자를 두 번째 매개변수로 받음
def detail(request, question_id):
    # 숫자에 해당하는 과목을 Question 테이블에서 받아와 question 변수에 지정
    question = get_object_or_404(Question, pk = question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question' : question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id=question.id)

def question_create(request):
    #  POST 방식으로 요청이 왔다면
    if request.method == 'POST':
        # 온 요청을 QuestionForm이 받아서 form에 저장
        # forms.py / model=Question
        form = QuestionForm(request.POST)
        # 폼의 유효성 검사
        # fields = ['subject', 'content'] 검사
        # Question 테이블에 'subject', 'content' 컬럼이 있는지 검사
        if form.is_valid():
            # 입력했던 내용들(subject, content)을 임시 저장
            question = form.save(commit=False)
            # 시간도 기록
            question.create_date = timezone.now()
            # 컬럼을 모두 채운 뒤 저장
            question.save()
            # 저장한 질문을 화면에 출력하기 위해 index에게 전달
            return redirect('pybo:index')
    # 만약 GET 방식으로 요청이 들어오면
    else:
        # 질문등록 화면으로 넘김
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
