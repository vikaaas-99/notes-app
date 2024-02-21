from datetime import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
import json
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model

# Create your views here.

### Template based views
# def signup(request):
#     return render(request, "signup.html")

# def login(request):
#     return render(request, "login.html")

# def create_new_user(request):
#     if request.method == "POST":
#         data = json.loads(request.body)

#         username = data["username"]
#         email = data["email"]
#         password = data["password"]

#         new_user, created = User.objects.get_or_create(username=username, email=email, password=password)
#         if created:
#             return JsonResponse({"message": "User created successfully"}, status=)
#         else:
#             return JsonResponse({"message": "User already exists"})


### APIs
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    data = request.data

    if not all(key in data.keys() for key in ["username", "email", "password"]):
        return Response({"message": "keys `username`, `email` and `password` are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    username = data["username"]
    email = data["email"]
    password = data["password"]

    new_user, created = get_user_model().objects.get_or_create(username=username, email=email, password=password)
    if created:
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "User already exists"}, status=status.HTTP_200_OK)
    

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login(request):
#     data = request.data

#     if not all("username", "password") in data.keys():
#         return Response({"message": "keys `username` and `password` are required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
#     username = data["username"]
#     password = data["password"]

#     user = User.objects.filter(username=username, password=password).first()
#     if user:
#         return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#     else:
#         return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(["POST"])
def create_note(request):
    user = request.user
    data = request.data

    if not all(key in data.keys() for key in ["title", "note"]):
        return Response({"message": "keys `title` and `note` are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    title = data["title"]
    note = data["note"]

    new_note = Notes.objects.create(user=user, title=title, note=note)
    return Response({"message": "Note created successfully", "note_id": new_note.id}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_note(request, id):
    user = request.user

    note = Notes.objects.filter(id=id, user=user).first()
    if note:
        return Response({"message": "Note found", "note": {"title": note.title, "note": note.note, "created_at": note.created_at}}, status=status.HTTP_200_OK)
    else:
        shared_note = SharedNotes.objects.filter(note__id=id, shared_with=user).first()
        if shared_note:
            return Response({"message": "Shared Note found", "note": {"title": shared_note.note.title, "note": shared_note.note.note, "created_at": shared_note.note.created_at}}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["PUT"])
def update_note(request, id):
    user = request.user
    data = request.data

    note = Notes.objects.filter(id=id, user=user).first()
    if note:
        if "title" in data.keys():
            note.title = data["title"]
        if "note" in data.keys():
            note.note = data["note"]
        note.save()

        log = LogNoteHistory.objects.create(note=note, updated_by=user)
    
        return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)
    else:
        shared_mote = SharedNotes.objects.filter(note__id=id, shared_with=user).first()
        if shared_mote:
            if "title" in data.keys():
                shared_mote.note.title = data["title"]
            if "note" in data.keys():
                shared_mote.note.note = data["note"]
            shared_mote.note.save()

            log = LogNoteHistory.objects.create(note=shared_mote.note, updated_by=user)
        
            return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["POST"])
def share_note_with_user(request):
    user = request.user
    data = request.data

    if not all(key in data.keys() for key in ["note_id", "share_with"]):
        return Response({"message": "keys `note_id` and `share_with` are required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    note_id = data["note_id"]
    username = data["share_with"]

    note = Notes.objects.filter(id=note_id, user=user).first()
    if note:
        user_to_share = get_user_model().objects.filter(username=username).first()
        if user_to_share:
            shared_note, created = SharedNotes.objects.get_or_create(note=note, shared_with=user_to_share)
            if created:
                return Response({"message": "Note shared successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Note already shared with the user"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
def get_note_version_history(request, id):
    user = request.user

    log = LogNoteHistory.objects.filter(note__id=id, note__user=user).order_by("-updated_at")
    if log:
        return Response({"message": "Note history found", "history": [{"tile": l.note.title, "note": l.note.note, "updated_at": l.updated_at, "updated_by": l.updated_by.username} for l in log]}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Note history not found"}, status=status.HTTP_404_NOT_FOUND) 