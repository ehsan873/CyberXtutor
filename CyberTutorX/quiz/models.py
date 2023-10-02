from django.db import models


# Create your models here.
class QuestionImage(models.Model):
    image = models.ImageField(upload_to="question\images")

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return ''


class QuestionSolutions(models.Model):
    question = models.TextField(max_length=3000, null=False, blank=False)
    answer = models.JSONField(null=False)


class TopicExplaination(models.Model):
    topic = models.TextField(max_length=3000, null=False, blank=False)
    explaintaion = models.TextField(null=False,blank=True,)
    for_class = models.TextField(max_length=3000, blank=True, null=True, default="")
    language = models.TextField(max_length=3000, blank=True, null=True, default="")
