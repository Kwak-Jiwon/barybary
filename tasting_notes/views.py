from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .models import YourModel, User, Coffee
import json


@csrf_exempt
@require_http_methods(["POST"])
def add_example(request):
    try:
        data = json.loads(request.body)
        new_entry = YourModel(
            written_id=data.get('written_id'),
            coffee_id=data.get('coffee_id'),
            note_floral=data.get('note_floral', False),
            note_fruit=data.get('note_fruit', False),
            note_berry=data.get('note_berry', False),
            note_nut=data.get('note_nut', False),
            note_choco=data.get('note_choco', False),
            note_cereal=data.get('note_cereal', False),
            taste_sweet=data.get('taste_sweet'),
            taste_sour=data.get('taste_sour'),
            taste_bitter=data.get('taste_bitter'),
            taste_body=data.get('taste_body'),
            overall_score=data.get('overall_score'),
            feeling=data.get('feeling', '')
        )
        new_entry.save()
        response = {
            'status': 'success',
            'message': 'Entry added successfully',
            'data': {
                '_id': str(new_entry._id),
                'written_id': new_entry.written_id,
                'coffee_id': new_entry.coffee_id,
                'note_floral': new_entry.note_floral,
                'note_fruit': new_entry.note_fruit,
                'note_berry': new_entry.note_berry,
                'note_nut': new_entry.note_nut,
                'note_choco': new_entry.note_choco,
                'note_cereal': new_entry.note_cereal,
                'taste_sweet': new_entry.taste_sweet,
                'taste_sour': new_entry.taste_sour,
                'taste_bitter': new_entry.taste_bitter,
                'taste_body': new_entry.taste_body,
                'overall_score': new_entry.overall_score,
                'feeling': new_entry.feeling
            }
        }
        return JsonResponse(response, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["GET"])
def get_examples(request):
    entries = YourModel.objects.all()
    data = [
        {
            '_id': str(entry._id),
            'written_id': entry.written_id,
            'coffee_id': entry.coffee_id,
            'note_floral': entry.note_floral,
            'note_fruit': entry.note_fruit,
            'note_berry': entry.note_berry,
            'note_nut': entry.note_nut,
            'note_choco': entry.note_choco,
            'note_cereal': entry.note_cereal,
            'taste_sweet': entry.taste_sweet,
            'taste_sour': entry.taste_sour,
            'taste_bitter': entry.taste_bitter,
            'taste_body': entry.taste_body,
            'overall_score': entry.overall_score,
            'feeling': entry.feeling
        }
        for entry in entries
    ]
    return JsonResponse({'status': 'success', 'data': data}, status=200)

@csrf_exempt
@require_http_methods(["POST"])
def add_user(request):
    try:
        data = json.loads(request.body)
        new_user = User(
            id=data.get('id'),
            name=data.get('name'),
            review_lst=data.get('review_lst', [])
        )
        new_user.save()
        response = {
            'status': 'success',
            'message': 'User added successfully',
            'data': {
                'id': new_user.id,
                'name': new_user.name,
                'review_lst': new_user.review_lst
            }
        }
        return JsonResponse(response, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["GET"])
def get_users(request):
    users = User.objects.all()
    data = [
        {
            'id': user.id,
            'name': user.name,
            'review_lst': user.review_lst
        }
        for user in users
    ]
    return JsonResponse({'status': 'success', 'data': data}, status=200)



@require_http_methods(["GET"])
def get_user_by_id(request, user_id):
    try:
        # Convert user_id to int if it's coming from a URL/path variable
        user_id = int(user_id)
        user = User.objects.get(id=user_id)
        data = {
            'id': user.id,
            'name': user.name,
            'review_lst': user.review_lst
        }
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid ID format'}, status=400)
    


@csrf_exempt
@require_http_methods(["POST"])
def add_review(request):
    try:
        data = json.loads(request.body)
        coffee_id = data['coffee_id']
        review = data['review']

        # Retrieve the specific Coffee instance
        coffee = Coffee.objects.get(_id=coffee_id)

        # Add the new review to the review_lst
        coffee.review_lst.append(review)
        coffee.save()

        # Prepare the response data
        response_data = {
            'id': coffee._id,
            'type': coffee.type,
            'name': coffee.name,
            'name_eng': coffee.name_eng,
            'script': coffee.script,
            'review_lst': coffee.review_lst
        }
        return JsonResponse({'status': 'success', 'message': 'Review added successfully', 'data': response_data}, status=200)
    except Coffee.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Coffee not found'}, status=404)
    except KeyError:
        return JsonResponse({'status': 'error', 'message': 'Missing coffee_id or review in request data'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_or_register(request):
    try:
        # Parse the JSON body of the request
        data = json.loads(request.body)
        user_id = data['id']
        name = data['name']

        # Check if the user already exists
        user, created = User.objects.get_or_create(id=user_id, defaults={'name': name})

        if created:
            # User was created
            status_message = "User registered successfully."
            status_code = 201
        else:
            # User already existed
            status_message = "User logged in successfully."
            status_code = 200

        # Prepare response data
        response_data = {
            'id': user.id,
            'name': user.name,
            'review_lst': user.review_lst
        }
        return JsonResponse({'status': 'success', 'message': status_message, 'data': response_data}, status=status_code)
    except KeyError:
        # Handle missing data in the request
        return JsonResponse({'status': 'error', 'message': 'Missing id or name in request data'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        # Generic exception handler for other unforeseen errors
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def add_coffee(request):
    try:
        data = json.loads(request.body)
        # new_id = Sequence.get_next_value('coffee_id')
        new_coffee = Coffee(
            type=data.get('type'),
            img = data.get('img'),  # 추가
            name=data.get('name'),
            name_eng=data.get('name_eng'),
            script=data.get('script'),
            review_lst=data.get('review_lst', [])
        )
        new_coffee.save()
        response = {
            'status': 'success',
            'message': 'Coffee added successfully',
            'data': {
                '_id': str(new_coffee._id),
                'img' : new_coffee.img,
                'type': new_coffee.type,
                'name': new_coffee.name,
                'name_eng': new_coffee.name_eng,
                'script': new_coffee.script,
                'review_lst': new_coffee.review_lst
            }
        }
        return JsonResponse(response, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["GET"])
def get_coffees(request):
    coffees = Coffee.objects.all()
    data = [
        {
            '_id': str(coffee._id),
            'img': coffee.img,
            'type': coffee.type,
            'name': coffee.name,
            'name_eng': coffee.name_eng,
            'script': coffee.script,
            'review_lst': coffee.review_lst
        }
        for coffee in coffees
    ]
    return JsonResponse({'status': 'success', 'data': data}, status=200)

@csrf_exempt
@require_http_methods(["POST"])
def edit_note(request):
    try:
        data = json.loads(request.body)
        note_id = data.get('_id')
        entry = YourModel.objects.get(_id=note_id)
        entry.written_id = data.get('written_id', entry.written_id)
        entry.coffee_id = data.get('coffee_id', entry.coffee_id)
        entry.note_floral = data.get('note_floral', entry.note_floral)
        entry.note_fruit = data.get('note_fruit', entry.note_fruit)
        entry.note_berry = data.get('note_berry', entry.note_berry)
        entry.note_nut = data.get('note_nut', entry.note_nut)
        entry.note_choco = data.get('note_choco', entry.note_choco)
        entry.note_cereal = data.get('note_cereal', entry.note_cereal)
        entry.taste_sweet = data.get('taste_sweet', entry.taste_sweet)
        entry.taste_sour = data.get('taste_sour', entry.taste_sour)
        entry.taste_bitter = data.get('taste_bitter', entry.taste_bitter)
        entry.taste_body = data.get('taste_body', entry.taste_body)
        entry.overall_score = data.get('overall_score', entry.overall_score)
        entry.feeling = data.get('feeling', entry.feeling)
        entry.save()
        response = {
            'status': 'success',
            'message': 'Entry updated successfully',
            'data': {
                '_id': str(entry._id),
                'written_id': entry.written_id,
                'coffee_id': entry.coffee_id,
                'note_floral': entry.note_floral,
                'note_fruit': entry.note_fruit,
                'note_berry': entry.note_berry,
                'note_nut': entry.note_nut,
                'note_choco': entry.note_choco,
                'note_cereal': entry.note_cereal,
                'taste_sweet': entry.taste_sweet,
                'taste_sour': entry.taste_sour,
                'taste_bitter': entry.taste_bitter,
                'taste_body': entry.taste_body,
                'overall_score': entry.overall_score,
                'feeling': entry.feeling
            }
        }
        return JsonResponse(response, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except YourModel.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Entry not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def remove_note(request):
    try:
        data = json.loads(request.body)
        note_id = data.get('_id')
        entry = YourModel.objects.get(_id=note_id)
        entry.delete()
        return JsonResponse({'status': 'success', 'message': 'Entry deleted successfully'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except YourModel.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Entry not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def add_user_review(request):
    try:
        data = json.loads(request.body)
        user_id = data['user_id']
        review = data['review']

        # Retrieve the specific User instance
        user = User.objects.get(id=user_id)

        # Add the new review to the review_lst
        user.review_lst.append(review)
        user.save()

        # Prepare the response data
        response_data = {
            'id': user.id,
            'name': user.name,
            'review_lst': user.review_lst
        }
        return JsonResponse({'status': 'success', 'message': 'Review added successfully', 'data': response_data}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except KeyError:
        return JsonResponse({'status': 'error', 'message': 'Missing user_id or review in request data'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)