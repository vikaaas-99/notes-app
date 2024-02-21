from django.urls import include, path

from .views import *

app_name = "notes"
urlpatterns = [
    path("create", create_note, name="create_note"),
    path("get/<int:id>", get_note, name="get_note"),
    path("share", share_note_with_user, name="share_note_with_user"),
    path("update/<int:id>", update_note, name="update_note"),
    path("version-history/<int:id>", get_note_version_history, name="get_note_version_history"),
]