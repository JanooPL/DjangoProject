from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my", views.index_my_view, name="index_my_view"),
    #rejestracja i logowanie:
    path("register", views.register_view, name="register_view"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("game/<uuid:game_id>/", views.game_view, name="game_view"),
    path("check_game_changes/<uuid:game_id>/", views.check_game_changes, name="check_game_changes"),
    path("reset/<uuid:game_id>/", views.reset_view, name="reset_view") ,
    path("out/<uuid:game_id>/", views.out_view, name="out_view") ,
]