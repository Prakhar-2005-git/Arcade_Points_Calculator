from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib import admin, messages
from .models import LeaderboardEntry
import os
import csv
from django.conf import settings

class CsvImportFormAdmin(forms.Form):
    csv_upload_form = forms.FileField()

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'total_points')
    search_fields = ('user_name',)
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_csv/', self.upload_csv, name='upload_csv')]
        return new_urls + urls
    
    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload_form"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, "Please upload a CSV file.")
                return HttpResponseRedirect(request.path_info)
            
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(settings.BASE_DIR, 'LeaderboardEntry', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Delete any existing CSV files
            for existing_file in os.listdir(upload_dir):
                if existing_file.endswith('.csv'):
                    os.remove(os.path.join(upload_dir, existing_file))
            
            # Save the new CSV file
            file_path = os.path.join(upload_dir, 'leaderboard_data.csv')
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
            
            # Call the sync command to process the CSV
            from django.core.management import call_command
            call_command('sync_leaderboard')
            
            messages.success(request, "CSV file uploaded and leaderboard updated successfully.")
            return redirect('..')
        
        form = CsvImportFormAdmin()
        data = {'form': form}
        return render(request, 'admin/upload_csv.html', data)
