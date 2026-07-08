# from django.contrib.auth.models import User
# from rest_framework import serializers
# from .models import *
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response

# # User = settings.AUTH_USER_MODEL


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'nama_lengkap', 'kelas', 'usia', 'kelamin', 'password', 'email', 'is_staff']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'username': {'required': True},
#             'email': {'required': True},
#             'is_staff': {'required': False},
#             'nama_lengkap': {'required': True},
#             'kelas': {'required': True},
#             'usia': {'required': True},
#             'kelamin': {'required': True},
#               # 'write_only' artinya password tidak akan
#                                              # dikirim balik di respon (biar aman)
#         }

#     def create(self, validated_data):
#         # Kita pakai create_user agar password-nya di-hash (dienkripsi)
#         # BUKAN disimpan sebagai teks biasa. Ini WAJIB!
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             nama_lengkap=validated_data['nama_lengkap'],
#             kelas=validated_data['kelas'],
#             usia=validated_data['usia'],
#             kelamin=validated_data['kelamin'],
#         )
#         return user
    
#     def update(self, instance, validated_data):
#         # Update username / email / is_staff
#         for attr, value in validated_data.items():
#             if attr == 'password':
#                 # pakai set_password agar di-hash
#                 instance.set_password(value)
#             else:
#                 setattr(instance, attr, value)

#         instance.save()
#         return instance

#     def validate(self, data):
#         emailData = data.get('email')
#         if emailData:
#             # Pastikan email unik, tetapi abaikan dirinya sendiri saat update
#             user_id = self.instance.id if self.instance else None
#             if User.objects.filter(email=emailData).exclude(id=user_id).exists():
#                 raise serializers.ValidationError("email udah ada")
#         return data

# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                             context={'request': request})
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)

#         return Response({
#             'token': token.key,
#             'user': UserSerializer(user).data
#         })
    

# # ===== SERIALIZER UNTUK SUBMIT TES =====
# class HasilTesSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = HasilTes
#         fields = [
#             'user',
#             'mtk', 'indo', 'ipa', 'ips',
#             'realistic', 'investigative', 'artistic',
#             'social', 'enterprising', 'conventional',
#             'logika', 'verbal', 'mekanikal',
#             'rekomendasi_akademik',
#             'rekomendasi_riasec',
#             'rekomendasi_bakat',
#             'rekomendasi_gabungan',
#             'created_at'
#         ]

#         read_only_fields = [
#             'user',
#             'rekomendasi_akademik',
#             'rekomendasi_riasec',
#             'rekomendasi_bakat',
#             'rekomendasi_gabungan',
#             'created_at'
#         ]

#     def create(self, validated_data):
#         user = self.context['request'].user

#         hasil = HasilTes.objects.create(
#             user=user,
#             rekomendasi_akademik='SMA - IPA',
#             rekomendasi_riasec='SMA - IPS',
#             rekomendasi_bakat='SMK - Akuntansi',
#             rekomendasi_gabungan='SMA - IPS',
#             **validated_data
#         )

#         return hasil


# # ===== SERIALIZER UNTUK RESPONSE =====
# class HasilTesResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HasilTes
#         fields = '__all__'


# # ===== SERIALIZER UNTUK DATA USER/SISWA =====
# class UserSiswaSerializer(serializers.ModelSerializer):
#     """Data dasar siswa (untuk list admin)"""
#     status_tes = serializers.SerializerMethodField()
#     rekomendasi = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'nama_lengkap', 'kelas', 'kelamin', 'status_tes', 'rekomendasi']

#     def get_status_tes(self, obj):
#         return 'Sudah Tes' if hasattr(obj, 'hasil_tes') else 'Belum Tes'

#     def get_rekomendasi(self, obj):
#         if hasattr(obj, 'hasil_tes'):
#             return obj.hasil_tes.rekomendasi_gabungan
#         return None


# class UserSiswaDetailSerializer(serializers.ModelSerializer):
#     """Data lengkap siswa + hasil tes"""
#     hasil_tes = HasilTesResponseSerializer(read_only=True)

#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'nama_lengkap', 'kelas', 'usia', 'kelamin',
#             'hasil_tes'
#         ]


from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# User = settings.AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'nama_lengkap',
            'kelas',
            'usia',
            'nip',
            'kelamin',
            'password',
            'email',
            'is_staff'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'allow_blank': True
            },
            'username': {'required': False},
            'email': {'required': False},
            'is_staff': {'required': False},
            'nama_lengkap': {'required': False, 'allow_blank': True},
            'kelas': {'required': False, 'allow_blank': True},
            'usia': {'required': False, 'allow_null': True},
            'kelamin': {'required': False, 'allow_blank': True},
            'nip': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            nama_lengkap=validated_data.get('nama_lengkap', ''),
            kelas=validated_data.get('kelas', ''),
            usia=validated_data.get('usia', None),
            kelamin=validated_data.get('kelamin', ''),
            nip=validated_data.get('nip', ''),
            is_staff=validated_data.get('is_staff', False),
        )

        if password:
            user.set_password(password)

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate(self, data):
        emailData = data.get('email')

        if emailData:
            user_id = self.instance.id if self.instance else None

            if User.objects.filter(email=emailData).exclude(id=user_id).exists():
                raise serializers.ValidationError({
                    "email": "Email sudah digunakan"
                })

        return data

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

# ===== SERIALIZER UNTUK SUBMIT TES =====
class HasilTesSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = HasilTes

        fields = [
            'id',
            'user',

            'mtk',
            'indo',
            'ipa',
            'ips',

            'realistic',
            'investigative',
            'artistic',
            'social',
            'enterprising',
            'conventional',

            'logika',
            'verbal',
            'mekanikal',

            'rekomendasi_akademik',
            'rekomendasi_riasec',
            'rekomendasi_bakat',
            'rekomendasi_gabungan',

            'created_at'
        ]

        read_only_fields = [
            'id',
            'user',
            'created_at'
        ]

    def create(self, validated_data):

        user = self.context['request'].user

        hasil = HasilTes.objects.create(
            user=user,

            # rekomendasi_akademik='SMA - IPA',
            # rekomendasi_riasec='SMA - IPS',
            # rekomendasi_bakat='SMK - Akuntansi',
            # rekomendasi_gabungan='SMA - IPS',

            **validated_data
        )

        return hasil

# ===== SERIALIZER UNTUK RESPONSE =====
class HasilTesResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = HasilTes

        fields = [
            'id',
            'user',

            'mtk',
            'indo',
            'ipa',
            'ips',

            'realistic',
            'investigative',
            'artistic',
            'social',
            'enterprising',
            'conventional',

            'logika',
            'verbal',
            'mekanikal',

            'rekomendasi_akademik',
            'rekomendasi_riasec',
            'rekomendasi_bakat',
            'rekomendasi_gabungan',

            'created_at'
        ]

# ===== SERIALIZER UNTUK DATA USER/SISWA =====
class UserSiswaSerializer(serializers.ModelSerializer):
    status_tes = serializers.SerializerMethodField()
    rekomendasi = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'nama_lengkap',
            'kelas',
            'kelamin',
            'status_tes',
            'rekomendasi'
        ]

    def get_status_tes(self, obj):
        return 'Sudah Tes' if hasattr(obj, 'hasil_tes') else 'Belum Tes'

    def get_rekomendasi(self, obj):
        if hasattr(obj, 'hasil_tes'):
            return obj.hasil_tes.rekomendasi_gabungan
        return None

class UserSiswaDetailSerializer(serializers.ModelSerializer):

    hasil_tes = HasilTesResponseSerializer(read_only=True)

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'nama_lengkap',
            'kelas',
            'usia',
            'kelamin',
            'hasil_tes'
        ]