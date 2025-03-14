from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ReportFolder, Report
from .forms import ReportFolderForm, ReportForm

@login_required
def folder_list(request):
    folders = ReportFolder.objects.filter(user=request.user)
    return render(request, 'folder_list.html', {'folders': folders})

@login_required
def folder_create(request):
    if request.method == 'POST':
        form = ReportFolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect('reports:folder_list')
    else:
        form = ReportFolderForm()
    return render(request, 'folder_create.html', {'form': form})

@login_required
def folder_detail(request, folder_id):
    folder = get_object_or_404(ReportFolder, pk=folder_id, user=request.user)
    reports = Report.objects.filter(folder=folder)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.folder = folder
            report.user = request.user
            report.save()
            return redirect('reports:folder_detail', folder_id=folder_id)
    else:
        form = ReportForm()

    return render(request, 'folder_detail.html', {'folder': folder, 'reports': reports, 'form': form})

@login_required
def report_delete(request, report_id):
    report = get_object_or_404(Report, pk=report_id, user=request.user)
    folder_id = report.folder.id
    report.delete()
    return redirect('reports:folder_detail', folder_id=folder_id)

@login_required
def folder_delete(request, folder_id):
    folder = get_object_or_404(ReportFolder, pk=folder_id, user=request.user)
    folder.delete()
    return redirect('reports:folder_list')