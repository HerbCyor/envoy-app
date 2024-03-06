from django.db import models
from users.models import MyUser

# Create your models here.


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / uploads / user_<id>/<filename>
    return f"uploads/user_{instance.user.id}/{filename}"


class FileRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    api_calls = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    input_file = models.FileField(upload_to=user_directory_path)
    output_file = models.FileField()

    # max_expected_calls
    # current_process = 0
    class Meta:
        get_latest_by = "date"

    def __str__(self):
        return f"{self.user}-{self.date}"
