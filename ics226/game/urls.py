from django.urls import path
from . import views

# django keyword ''default(root url), calling views.index
urlpatterns = [
    path('', views.show_board, name='board_show'),
    path('greet/<str:name>', views.greet, name='greet'),
    path('create/', views.create_board, name='board_create'),
    path('display/<int:player_id>/', views.get_player, name='player'),
    path('move/<str:player_id>', views.move_player, name='move'),
]

