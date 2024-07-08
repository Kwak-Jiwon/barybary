# views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserContact, UserResidence

@csrf_exempt
def save_user_contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_contact = UserContact(
                name=data.get('name'),
                number=data.get('number'),
                phone=data.get('phone')
            )
            user_contact.save()
            return HttpResponse("User contact saved successfully!")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def save_user_residence(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_residence = UserResidence(
                name=data.get('name'),
                room_number=data.get('room_number'),
                address=data.get('address')
            )
            user_residence.save()
            return HttpResponse("User residence saved successfully!")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
