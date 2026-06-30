from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    nama_lengkap = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)
    usia = models.IntegerField(null=True, blank=True)
    kelamin = models.CharField(max_length=10)

class HasilTes(models.Model):
    """
    Satu table untuk menyimpan SEMUA hasil tes siswa.
    Nilai yang disimpan adalah nilai MENTAH (sudah berupa angka),
    bukan jawaban per soal.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hasil_tes'
    )
    # ===== AKADEMIK (nilai 1-3) =====
    mtk = models.IntegerField()
    indo = models.IntegerField()
    ipa = models.IntegerField()
    ips = models.IntegerField()
    # mtk = models.IntegerField(choices=[(3, 'Tinggi'), (2, 'Sedang'), (1, 'Rendah')])
    # indo = models.IntegerField(choices=[(3, 'Tinggi'), (2, 'Sedang'), (1, 'Rendah')])
    # ipa = models.IntegerField(choices=[(3, 'Tinggi'), (2, 'Sedang'), (1, 'Rendah')])
    # ips = models.IntegerField(choices=[(3, 'Tinggi'), (2, 'Sedang'), (1, 'Rendah')])

    # ===== RIASEC (nilai 5-25, hasil penjumlahan 5 soal per dimensi) =====
    realistic = models.IntegerField()   # Realistic
    investigative = models.IntegerField()   # Investigative
    artistic = models.IntegerField()   # Artistic
    social = models.IntegerField()   # Social
    enterprising = models.IntegerField()   # Enterprising
    conventional = models.IntegerField()   # Conventional

    # ===== BAKAT (nilai 0-5, jumlah jawaban benar per kategori) =====
    logika = models.IntegerField()
    verbal = models.IntegerField()
    mekanikal = models.IntegerField()

    # ===== REKOMENDASI (hasil akhir) =====
    rekomendasi_akademik = models.CharField(max_length=100)
    rekomendasi_riasec = models.CharField(max_length=100)
    rekomendasi_bakat = models.CharField(max_length=100)
    rekomendasi_gabungan = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hasil Tes {self.user.nama_lengkap} - {self.rekomendasi_gabungan}"

    class Meta:
        verbose_name = "Hasil Tes"
        verbose_name_plural = "Hasil Tes"