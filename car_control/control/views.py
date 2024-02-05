# control/views.py
from django.shortcuts import render
from django.http import JsonResponse

def forward(request):
    # 여기에 자동차를 전진시키는 코드를 추가
    return JsonResponse({'status': 'forward success'})

def backward(request):
    # 여기에 자동차를 후진시키는 코드를 추가
    return JsonResponse({'status': 'backward success'})

def index(request):
    return render(request, 'control/index.html')
