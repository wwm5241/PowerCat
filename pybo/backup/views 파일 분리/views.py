#fromm django.http import HttpResponse
# html 파일로 전달 역할을 하는 render
# 응답에 요청을 한 경우 404 not found 에러 처리 역할을 하는 get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, Comment
from django.utils import timezone # timezone 기능 추가
from .forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# 응답에 대한 처리 함수를 정의할 때 무조건 매개변수 한 개 이상 필요
def index(request): # request 인자는 필수
    ## 요청을 딕셔너리 형태로 받아 페이지화
    ## url 주소 뒤에 숫자가 붙지 않는 기본 페이지를 나타내는 숫자 1을 두번째 인자로 대입
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-subject') # -subject는 subject기준으로 역순으로 조회
    ## 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    ## question_list가 가공된 상태이기 때문에 따로 넘겨주지 않아도 됨
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context) # render를 사용하면 많은양의 데이터를 전달할 때 사용한다(추후 view와 template가 주고 싶을때도 render 사용)

## urls.py에서 넘겨받은 숫자를 두번째 매개변수로 받음
def detail(request, question_id):
    ## 숫자에 해당하는 과목을 Question 테이블에서 받아와 question 변수에 지정
    question = get_object_or_404(Question, pk=question_id) # Question 테이블의 objects를 id=question_id로 get하겠다
    context = {'question': question} # 키와 값으로 위의 question 키를 값으로 넣겠다
    return render(request,'pybo/question_detail.html', context)

# 답변 생성 함수
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id) # 요청하는 부분이 있는지 없는지 지정 = 위에 detail과 동일
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            # author 속성에 로그인 계정 저장
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

# 질문 생성 함수
@login_required(login_url='common:login')
def question_create(request):
    # POST 방식으로 요청이 왔다면 
    if request.method == 'POST':
        ## 온 요청을 QuestionForm이 받아서 form에 저장
        ## forms.py / model=Question 으로 만들었다
        form = QuestionForm(request.POST) # 장고는 POST로 동작
        ## forms.py와의 폼 유효성 검사 => forms.py는 유효성 검사를 위한 폼을 만들었기 때문
        ## fields = ['subject', 'content'] 검사
        ## Question 테이블에 'subject', 'content' 컬럼이 있는지
        if form.is_valid(): # Question 테이블에 'subject', 'content' 컬럼이 있어 form이 유효하다면
            ## 입력했던 내용들('subject', 'content')을 임시 저장
            question = form.save(commit=False) # question을에 임시저장하겠다
            # author 속성에 로그인 계정 저장
            question.author = request.user 
            ## 시간도 기록
            question.create_date = timezone.now()
            ## 컬럼을 모두 채운 뒤에 저장 => 'subject', 'content' 그리고 시간
            question.save() # 임시저장과 create_date를 동시에 저장
            ## 저장한 질문을 화면에 출력하기 위해 index에게 전달
            return redirect('pybo:index') # 새로운 페이지가 아니니 redirect하고 ~/pybo/index로 넘기겠다
        ## 만약 GET 방식으로 요청이 들어온면?
    else: # POST가 아닌 방식이 온다면? = GET방식이 온다면?
            ## 질문 등록 화면으로 넘김
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# 질문 수정 함수
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# 질문 삭제 함수
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

# 답변 수정 함수
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

# 답변 삭제 함수
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

# 질문 댓글 등록 함수
@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id) # 요청하는 부분이 있는지 없는지 지정 = 위에 detail과 동일
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 질문 댓글 수정 함수
@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 질문 댓글 삭제 함수
@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)

# 답변 댓글 등록 함수
@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id) # 요청하는 부분이 있는지 없는지 지정 = 위에 detail과 동일
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 답변 댓글 수정 함수
@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 답변 댓글 삭제 함수
@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)