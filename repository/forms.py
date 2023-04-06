import requests

from django import forms
from .models import Project, Tag


class ProjectForm(forms.ModelForm):

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

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        choices = self.fields["tags"].widget.choices

        self.fields["tags"].widget = forms.CheckboxSelectMultiple(
            choices=choices
        )
        for key in self.fields:
            self.fields[key].widget.attrs = {
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }

        # Sort Fileds Alphabetically
        self.fields["department"].queryset = self.fields["department"].queryset.order_by(
            'name')
        self.fields["institution"].queryset = self.fields["institution"].queryset.order_by(
            'name')
        self.fields["tags"].queryset = self.fields["tags"].queryset.order_by(
            'name')

        self.fields["title"].widget.attrs["placeholder"] = "Hospital management system..."
        self.fields["year_published"].widget.attrs["placeholder"] = "2019"
        self.fields["supervisor"].widget.attrs["placeholder"] = "Albert Einstein"
        self.fields["url"].widget.attrs["placeholder"] = "Enter a valid URL"
        self.fields["description"].widget.attrs["placeholder"] = "This is a system designed to model other systems..."

    def clean(self):
        return self.cleaned_data

    def save(self):

        tags = self.cleaned_data.pop("tags")
        post = Project(**self.cleaned_data, scholar=self.request.user)

        # !!! REMOVE THIS BLOCK LATER

    #     requests.post("https://api.unicheck.com/oauth/access-token",
    #                   headers={
    #                       "Content-Type": "application/x-www-form-urlencoded"},
    #                   data={
    #                       "grant_type": "client_credentials",
    #                       ""
    #                   }
    #                   )

    # -d 'grant_type=<grant_type>&client_id=<client_id>&client_secret=<secret>'
        post.plagiarism_score = 0
    #   # !!! REMOVE THIS BLOCK LATER

        post.save()

        for tag in tags:
            post.tags.add(tag)

        return post


class UpdateProjectForm(forms.ModelForm):

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

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        choices = self.fields["tags"].widget.choices

        self.fields["tags"].widget = forms.CheckboxSelectMultiple(
            choices=choices
        )
        for key in self.fields:
            self.fields[key].widget.attrs = {
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }

        # Sort Fileds Alphabetically
        self.fields["department"].queryset = self.fields["department"].queryset.order_by(
            'name')
        self.fields["institution"].queryset = self.fields["institution"].queryset.order_by(
            'name')
        self.fields["tags"].queryset = self.fields["tags"].queryset.order_by(
            'name')

        self.fields["title"].widget.attrs["placeholder"] = "Hospital management system..."
        self.fields["year_published"].widget.attrs["placeholder"] = "2019"
        self.fields["supervisor"].widget.attrs["placeholder"] = "Albert Einstein"
        self.fields["url"].widget.attrs["placeholder"] = "Enter a valid URL"
        self.fields["description"].widget.attrs["placeholder"] = "This is a system designed to model other systems..."

    def clean(self):
        return self.cleaned_data
