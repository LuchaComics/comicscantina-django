import os
import sys
from django.conf import settings
from api.models.gcd.story import GCDStory
from api.models.gcd.issue import GCDIssue

class ImportGenre:
    """
        Class is responsible by iterating through the "Story" model
        and copying the 'genre' column into the "Issue" 'genre' column.
    """
    def __init__(self):
        pass
    
    def begin_import(self):
        print("ImportGenre: Initializing")
        # Iterate through all the stories and update their issues.
        stories = GCDStory.objects.all()
        print("ImportGenre: Beginning")
        for story in stories:
            issue_id = story.issue_id
            genre = story.genre

            # Fetch the issue and update the 'genre' and then save
            try:
                print("ImportGenre: Updating Issue: " + str(issue_id))
                issue = GCDIssue.objects.get(issue_id=issue_id)
                issue.genre = genre
                issue.save()
            except GCDIssue.DoesNotExist:
                pass
        print("ImportGenre: Finished")