from django.shortcuts import render
from django.http import JsonResponse
from .car_control import car

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
    time.sleep(1)
    return JsonResponse({'status': 'left turn success'})

def right(request):
    mycar.servo_right()
    time.sleep(1)
    return JsonResponse({'status': 'right turn success'})

def stop(request):
    mycar.motor_stop()
    time.sleep(1)
    return JsonResponse({'status': 'stop success'})

def index(request):
    return render(request, 'control/index.html')
