from django.db import models
import datetime


class AbstractBaseModel(models.Model):

   created = models.DateTimeField(editable=False)
   modified = models.DateTimeField()

   class Meta:
       abstract = True

   def save(self, *args, **kwargs):
       ''' On save, update timestamps '''
       if not self.id:
           self.created = datetime.datetime.today()
       self.modified = datetime.datetime.today()
       super(AbstractBaseModel, self).save(*args, **kwargs)
 
