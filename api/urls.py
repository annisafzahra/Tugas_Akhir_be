# from django.urls import path
# from .views import *
# from rest_framework.authtoken.views import obtain_auth_token

# urlpatterns = [
#     path('login/', CustomAuthToken.as_view(), name='api_login'),
#     path('user/create/', RegisterView.as_view(), name='api_create_user'),
#     path('user/get/', GetListUserView.as_view(), name='api_get_list_user'),
#     path('tes/hasil/', GetListUserView.as_view(), name='api_get_list_user'),

#     # ===== ENDPOINT SISWA =====
#     path('tes/submit/', views.submit_tes, name='submit-tes'),
#     path('tes/hasil/', views.get_hasil_siswa, name='hasil-siswa'),
    
#     # ===== ENDPOINT ADMIN =====
#     path('admin/siswa/', views.admin_list_siswa, name='admin-list-siswa'),
#     path('admin/siswa/<int:user_id>/', views.admin_detail_siswa, name='admin-detail-siswa'),
# ]






# from django.urls import path
# from .views import *

# urlpatterns = [
#     # AUTH
#     path('login/', CustomAuthToken.as_view(), name='api_login'),
#     path('user/create/', RegisterView.as_view(), name='api_create_user'),
#     path('user/get/', GetListUserView.as_view(), name='api_get_list_user'),

#     # ===== ENDPOINT SISWA =====
#     path('tes/submit/', SubmitHasilTesView.as_view(), name='submit-tes'),
#     path('tes/get/', GetHasilTesView.as_view(), name='get-tes'),
#     path('tes/hasil/', get_hasil_siswa, name='hasil-siswa'),

#     # ===== ENDPOINT ADMIN =====
#     path('admin/siswa/', admin_list_siswa, name='admin-list-siswa'),
#     path('admin/siswa/<int:user_id>/', admin_detail_siswa, name='admin-detail-siswa'),
# ]



from django.urls import path
from .views import *

urlpatterns = [
    # AUTH
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('user/create/', RegisterView.as_view(), name='api_create_user'),
    path('user/get/', GetListUserSiswaView.as_view(), name='api_get_list_user'),
    path('user/detail/<int:id>/', GetDetailUserSiswaView.as_view(), name='api_get_detail_user'),

    # ===== ENDPOINT SISWA =====
    path('tes/submit/', SubmitHasilTesView.as_view(), name='submit-tes'),
    path('tes/get/', GetHasilTesView.as_view(), name='get-tes'),
    path('tes/hasil/', get_hasil_siswa, name='hasil-siswa'),

    # ===== ENDPOINT ADMIN =====
    path('admin/siswa/', GetListUserSiswaView.as_view(), name='admin-list-siswa'),
    path('admin/siswa/<int:user_id>/', admin_detail_siswa, name='admin-detail-siswa'),
    path('admin/delete-user/<int:id>/', DeleteUserSiswaView.as_view(), name='delete-user'),
    path('admin/update-user/<int:id>/', UpdateUserSiswaView.as_view(), name='update-user'),

    # ===== DELETE HASIL TES =====
    path('admin/delete-hasil/<int:id>/', DeleteHasilTesView.as_view(), name='delete-hasil-tes'),
]