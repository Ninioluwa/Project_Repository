from django import forms
from .models import Project, Tag

class ProjectForm(forms.ModelForm):

    tags = forms.ModelChoiceField(Tag.objects.all())
    class Meta:
        model = Project
        fields = [
            "title",
            "institution",
            "description",
            "year_published",
            "url",
            "department",
            "supervisor",
            "document",
            "cover_page",
            "tags"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        
        self.fields["title"].widget.attrs["placeholder"] = "Hospital management system..."
        self.fields["year_published"].widget.attrs["placeholder"] = "2019"
        self.fields["supervisor"].widget.attrs["placeholder"] = "Albert Einstein"
        self.fields["url"].widget.attrs["placeholder"] = "Enter a valid URL"
        self.fields["description"].widget.attrs["placeholder"] = "This is a system designed to model other systems..."

    
    def clean(self):
        return self.cleaned_data

    def save(self):
        pass