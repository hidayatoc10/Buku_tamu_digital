import sys
from django.contrib import admin
from guest.models import Guest
from import_export.admin import ImportExportModelAdmin
from cryptography.fernet import Fernet, InvalidToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

csrf_protect_m = method_decorator(csrf_protect)

class GuestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'name', 'jenis_kelamin', 'kategori_dituju', 'pihak_dituju', 'keperluan', 'foto')
    actions = ['encrypt_data', 'decrypt_data']
    readonly_fields = ("created_at", "updated_at", "key")
    list_filter = ["created_at", "jenis_kelamin", "kategori_dituju", "pihak_dituju",]

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Pilih salah satu aksi'}
        return super().changelist_view(request, extra_context=extra_context)

    def encrypt_data(self, request, queryset):
        for data in queryset:
            try:
                if not data.key:
                    data.key = Fernet.generate_key().decode()
                    data.save()
                print("Kunci sebelum enkripsi untuk ID {}: {}".format(data.id, data.key))
                data.save()
                print("Kunci setelah enkripsi untuk ID {}: {}".format(data.id, data.key))  # Debugging: Cetak kunci setelah enkripsi
            except Exception as e:
                print("Kesalahan dalam enkripsi data untuk ID {}: {}".format(data.id, str(e)))  # Debugging: Cetak pesan kesalahan
                self.message_user(request, "Gagal melakukan enkripsi data untuk ID {}.".format(data.id))
        self.message_user(request, "Data berhasil dienkripsi.")

    def decrypt_data(self, request, queryset):
        for data in queryset:
            try:
                if data.key:
                    print("Mendekripsi data untuk ID {}: Kunci - {}".format(data.id, data.key))
                    cipher_suite = Fernet(data.key.encode())
                    print("Data Terenkripsi: ", data.no_hp)
                    no_hp_decrypted = cipher_suite.decrypt(data.no_hp.encode())
                    # Pastikan dekoding yang tepat
                    data.no_hp = no_hp_decrypted.decode('utf-8')  # Sesuaikan encoding jika diperlukan
                    data.save()
                    self.message_user(request, f"Data berhasil didekripsi untuk ID {data.id}")
                else:
                    self.message_user(request, f"Kunci tidak ditemukan untuk data dengan ID {data.id}")
            except InvalidToken as e:
                self.message_user(request, f"Gagal mendekripsi data untuk ID {data.id}. Data mungkin rusak atau kunci tidak valid.")
                print(f"Kesalahan dalam mendekripsi data untuk ID {data.id}: {str(e)}")
            except Exception as e:
                self.message_user(request, f"Gagal mendekripsi data untuk ID {data.id}. Terjadi kesalahan.")
                print(f"Kesalahan dalam mendekripsi data untuk ID {data.id}: {str(e)}")

    encrypt_data.short_description = "Enkripsi Data Terpilih"
    decrypt_data.short_description = "Dekripsi Data Terpilih"
    admin.site.site_header = "Administrasi Buku Tamu"

admin.site.register(Guest, GuestAdmin)