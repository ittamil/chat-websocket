from django.db import models
# from accounts.models import User
from django.contrib.auth.models import User

class Thread(models.Model):
    threadname = models.CharField(max_length=200,null=True,blank=True)
    group = models.ManyToManyField(User,blank=True)
    
    def __str__(self):
        return str(self.threadname)

class ChatMessage(models.Model):
    
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message