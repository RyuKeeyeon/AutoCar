from django.shortcuts import render
from django.http import JsonResponse
from .car_control import car
import time
# Initialize the car outside the view functions to avoid reinitialization on each request
mycar = car()

def forward(request):
    mycar.motor_forward()
    time.sleep(1)
    return JsonResponse({'status': 'forward success'})

def backward(request):
    mycar.motor_reverse()
    time.sleep(1)
    return JsonResponse({'status': 'backward success'})

def left(request):
    global mycar
    mycar.servo_left()  # 좌회전을 위한 서보 모터 조정
    mycar.motor_forward()  # 전진 명령
    time.sleep(1)  # 필요한 회전 시간 대기
    mycar.servo_center()  # 서보 모터 중앙으로 재조정
    return JsonResponse({'status': '좌회전 성공'})

def right(request):
    global mycar
    mycar.servo_right()  # 우회전을 위한 서보 모터 조정
    mycar.motor_forward()  # 전진 명령
    time.sleep(1)  # 필요한 회전 시간 대기
    mycar.servo_center()  # 서보 모터 중앙으로 재조정
    return JsonResponse({'status': '우회전 성공'})


def stop(request):
    mycar.motor_stop()
    time.sleep(1)
    return JsonResponse({'status': 'stop success'})

def index(request):
    return render(request, 'control/index.html')


def remote(request):
    return render(request, 'control/remote.html')
