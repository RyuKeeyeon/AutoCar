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
    mycar.servo_left()
    time.sleep(1)  # 서보 모터를 왼쪽으로 회전시킨 후
    mycar.motor_forward()  # 자동차를 전진시킵니다.
    time.sleep(1)  # 실제 환경에서는 이 시간을 조정하여 원하는 회전 각도를 얻을 수 있습니다.
    mycar.servo_center()  # 회전 후에는 서보 모터를 다시 중앙으로 조정합니다.
    return JsonResponse({'status': 'left turn success'})

def right(request):
    mycar.servo_right()
    time.sleep(1)  # 서보 모터를 오른쪽으로 회전시킨 후
    mycar.motor_forward()  # 자동차를 전진시킵니다.
    time.sleep(1)  # 실제 환경에서는 이 시간을 조정하여 원하는 회전 각도를 얻을 수 있습니다.
    mycar.servo_center()  # 회전 후에는 서보 모터를 다시 중앙으로 조정합니다.
    return JsonResponse({'status': 'right turn success'})


def stop(request):
    mycar.motor_stop()
    time.sleep(1)
    return JsonResponse({'status': 'stop success'})

def index(request):
    return render(request, 'control/index.html')
