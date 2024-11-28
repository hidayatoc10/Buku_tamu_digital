import base64
import re
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views import View
from guest.models import Guest

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class FormView(View):
    def get(self, request):
        return render(request, 'form.html')

    def post(self, request):
        if request.method == "POST":
            name = request.POST.get('name', '')
            jenis_kelamin = request.POST.get('jenis_kelamin', '')
            kategori_dituju = request.POST.get('kategori_dituju', '')
            pihak_dituju = request.POST.get('pihak_dituju', '')
            keperluan = request.POST.get('keperluan', '')
            no_hp = request.POST.get('no_hp', '')
            foto_base64 = request.POST.get('foto', '')
            if not foto_base64:
                return render(request, 'form.html', {'error': 'Foto tidak boleh kosong'})

            try:
                format, imgstr = foto_base64.split(';base64,')
                ext = format.split('/')[-1]
                data = base64.b64decode(imgstr)
                
                foto = ContentFile(data, name=f'{name}.{ext}')
                obj = Guest.objects.create(
                    name=name,
                    jenis_kelamin=jenis_kelamin,
                    kategori_dituju=kategori_dituju,
                    pihak_dituju=pihak_dituju,
                    keperluan=keperluan,
                    no_hp=no_hp,
                    foto=foto
                )
                obj.save()
                
                return redirect('/')
            except Exception as e:
                return render(request, 'form.html', {'error': f'Error: {str(e)}'})
