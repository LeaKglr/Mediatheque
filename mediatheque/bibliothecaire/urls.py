from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_menu, name='library_menu'),
    path('create-member-borrower/', views.create_member_borrower, name='create_member_borrower'),
    path('update-member-borrower/<int:member_id>/', views.update_member_borrower, name='update_member_borrower'),
    path('members-list', views.members_list, name='members_list'),
    path('media-list/', views.media_list, name='media_list'),
    path('delete-member-borrower/<int:member_id>/', views.delete_member_borrower, name='delete_member_borrower'),
    path('create-member/', views.create_member_borrower, name='create_member'),
    path('add-book/', views.add_book, name='add_book'),
    path('add-dvd/', views.add_dvd, name='add_dvd'),
    path('add-cd/', views.add_cd, name='add_cd'),
    path('borrow-list/', views.borrow_list, name='borrow_list'),
    path('return-borrow/<int:borrow_id>/', views.return_borrow, name='return_borrow'),
    path('create-borrow/<int:member_id>/', views.create_borrow, name='create_borrow'),
    path('add-boardgame/', views.add_boardgame, name='add_boardgame'),
]