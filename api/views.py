from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from .helpers import *
from .models import *
from .serializers import *
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
# from sklearn.cluster import KMeans
# import numpy as np

from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

# from django.conf import settings

# User = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model

User = get_user_model()

import os
import pickle
from django.conf import settings

def load_model():
    path = os.path.join(settings.BASE_DIR, "api/ml/kmeans_model.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

def load_scaler():
    path = os.path.join(settings.BASE_DIR, "api/ml/scaler.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

def load_model_riasec():
    path = os.path.join(settings.BASE_DIR, "api/ml/kmeans_model_riasec.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

def load_scaler_riasec():
    path = os.path.join(settings.BASE_DIR, "api/ml/scaler_riasec.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

def load_model_bakat():
    path = os.path.join(settings.BASE_DIR, "api/ml/kmeans_model_bakat.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

def load_scaler_bakat():
    path = os.path.join(settings.BASE_DIR, "api/ml/scaler_bakat.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

# Create your views here.
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserSerializer``
#     authentication_classes = [TokenAuthentication]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class GetListUserSiswaView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=False)
    
class GetDetailUserSiswaView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

class DeleteUserSiswaView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_staff=False)
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()

        return Response(
            {
                "message": "User berhasil dihapus"
            },
            status=status.HTTP_200_OK
        )
    
class UpdateUserSiswaView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "User berhasil diupdate",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

# class SubmitHasilTesView(generics.CreateAPIView):
#     queryset = HasilTes.objects.all()
#     permission_classes = [IsAuthenticated]  # tetap AllowAny
#     serializer_class = HasilTesSerializer


class SubmitHasilTesView(generics.CreateAPIView):
    queryset = HasilTes.objects.all()
    serializer_class = HasilTesSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # =========================
        # 1. ambil data akademik
        # =========================
        akademik = pd.DataFrame([{
            "MTK": int(data["mtk"]),
            "Bahasa": int(data["indo"]),
            "IPA": int(data["ipa"]),
            "IPS": int(data["ips"]),
        }])
        
        riasec = pd.DataFrame([{
            "Realistic": int(data["realistic"]),
            "Investigative": int(data["investigative"]),
            "Artistic": int(data["artistic"]),
            "Social": int(data["social"]),
            "Enterprising": int(data["enterprising"]),
            "Conventional": int(data["conventional"])
        }])
        
        bakat = pd.DataFrame([{
            "Logika": int(data["logika"]),
            "Verbal": int(data["verbal"]),
            "Mekanikal": int(data["mekanikal"]),
        }])

        # =========================
        # 2. load scaler & model
        # =========================
        scaler = load_scaler()
        model = load_model()
        scaler_riasec = load_scaler_riasec()
        model_riasec = load_model_riasec()
        scaler_bakat = load_scaler_bakat()
        model_bakat = load_model_bakat()

        # =========================
        # 3. scaling + predict
        # =========================
        akademik_scaled = scaler.transform(akademik)
        cluster = model.predict(akademik_scaled)[0]
        riasec_scaled = scaler_riasec.transform(riasec)
        cluster_riasec = model_riasec.predict(riasec_scaled)[0]
        bakat_scaled = scaler_bakat.transform(bakat)
        cluster_bakat = model_bakat.predict(bakat_scaled)[0]

        # =========================
        # 4. mapping cluster
        # =========================
        mapping = {
            0: "IPA",
            1: "TKJ",
            2: "AKL",
            3: "IPS",
            4: "Bahasa",
            5: "TKRO"
        }

        rekomendasi_akademik = mapping.get(cluster, "Unknown")
        rekomendasi_riasec = mapping.get(cluster_riasec, "Unknown")
        rekomendasi_bakat = mapping.get(cluster_bakat, "Unknown")

        scores = {}

        scores[rekomendasi_akademik] = scores.get(rekomendasi_akademik, 0) + 0.4
        scores[rekomendasi_riasec] = scores.get(rekomendasi_riasec, 0) + 0.35
        scores[rekomendasi_bakat] = scores.get(rekomendasi_bakat, 0) + 0.25
        
        rekomendasi_gabungan = max(scores, key=scores.get)

        # =========================
        # 5. inject hasil ML
        # =========================
        data["rekomendasi_akademik"] = rekomendasi_akademik
        data["rekomendasi_riasec"] = rekomendasi_riasec
        data["rekomendasi_bakat"] = rekomendasi_bakat
        data["rekomendasi_gabungan"] = rekomendasi_gabungan

        # =========================
        # 6. save ke database
        # =========================
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)

        return Response(
            {
                "message": "Hasil tes berhasil disimpan",
                "cluster": int(cluster),
                "rekomendasi_akademik": rekomendasi_akademik,
                "rekomendasi_riasec": rekomendasi_riasec,
                "rekomendasi_bakat": rekomendasi_bakat,
                "rekomendasi_gabungan": rekomendasi_gabungan,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class GetHasilTesView(generics.ListAPIView):
    queryset = HasilTes.objects.all()
    permission_classes = [IsAuthenticated]  # tetap AllowAny
    serializer_class = HasilTesSerializer


# ===== SUBMIT HASIL TES (SISWA) =====
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_tes(request):
    """
    Endpoint untuk menyimpan hasil tes siswa.
    Hanya bisa diakses oleh siswa yang sudah login.
    """
    user = request.user

    # Cek apakah user adalah admin (admin tidak boleh submit tes)
    if user.is_staff:
        return Response(
            {'error': 'Admin tidak dapat mengisi tes.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Cek apakah siswa sudah pernah tes
    if hasattr(user, 'hasil_tes'):
        return Response(
            {'error': 'Kamu sudah menyelesaikan tes sebelumnya. Tidak bisa mengulangi.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = HasilTesSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        hasil = serializer.save()

        # Return response dengan data lengkap
        response_serializer = HasilTesResponseSerializer(hasil)
        return Response({
            'message': 'Hasil tes berhasil disimpan!',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===== GET HASIL TES SISWA YANG SEDANG LOGIN =====
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hasil_siswa(request):
    """
    Endpoint untuk siswa melihat hasil tesnya sendiri.
    """
    user = request.user

    if user.is_staff:
        return Response(
            {'error': 'Admin tidak memiliki hasil tes.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not hasattr(user, 'hasil_tes'):
        return Response(
            {'error': 'Kamu belum menyelesaikan tes.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = HasilTesResponseSerializer(user.hasil_tes)
    return Response({
        'message': 'Data hasil tes berhasil diambil.',
        'data': serializer.data
    })


# ===== ADMIN: LIST SEMUA SISWA =====
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_list_siswa(request):
    """
    Endpoint untuk admin/guru BK melihat daftar semua siswa.
    """
    if not request.user.is_staff:
        return Response(
            {'error': 'Hanya admin yang bisa mengakses halaman ini.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Ambil semua user yang BUKAN admin
    siswa_list = User.objects.filter(is_staff=False).order_by('-date_joined')
    serializer = UserSiswaSerializer(siswa_list, many=True)
    return Response({
        'message': 'Data siswa berhasil diambil.',
        'total': siswa_list.count(),
        'data': serializer.data
    })


# ===== ADMIN: DETAIL SISWA =====
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_detail_siswa(request, user_id):
    """
    Endpoint untuk admin melihat detail hasil tes siswa tertentu.
    """
    if not request.user.is_staff:
        return Response(
            {'error': 'Hanya admin yang bisa mengakses halaman ini.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Cari siswa, pastikan bukan admin
    siswa = get_object_or_404(User, id=user_id, is_staff=False)

    if not hasattr(siswa, 'hasil_tes'):
        return Response(
            {'error': 'Siswa ini belum menyelesaikan tes.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = UserSiswaDetailSerializer(siswa)
    return Response({
        'message': 'Detail hasil tes siswa berhasil diambil.',
        'data': serializer.data
    })

class DeleteHasilTesView(generics.DestroyAPIView):
    queryset = HasilTes.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = HasilTesSerializer
    lookup_field = 'id'

# ===== ADMIN: DELETE HASIL TES =====
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_hasil_tes(request, hasil_id):

    # Cek admin
    if not request.user.is_staff:
        return Response(
            {'error': 'Hanya admin yang bisa menghapus data.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Cari hasil tes berdasarkan id
    hasil_tes = get_object_or_404(HasilTes, id=hasil_id)

    # Hapus data
    hasil_tes.delete()

    return Response({
        'message': 'Hasil tes berhasil dihapus.'
    }, status=status.HTTP_200_OK)