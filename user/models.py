


from django.db import models
import uuid


# Create your models here.

class user(models.Model):

   username = models.CharField(max_length=30)
   password = models.CharField(max_length=100)
   phonenumber = models.CharField(max_length=10,primary_key=True)


      

      

      

      



class hotel(models.Model):
   hotel_id =models.CharField(primary_key = True,max_length=9)
   hotel_name = models.CharField(max_length=30)
   hotel_location = models.CharField(max_length=30)
   phonenumber = models.CharField(max_length=10)
  
class hotel_type(models.Model):
    hotel_id = models.ForeignKey(hotel,on_delete=models.CASCADE)
    typeofroom = models.CharField(max_length=30)
    hotel_room = models.IntegerField()
    hotel_price = models.IntegerField(default=1000)
    img=models.ImageField()
   

class availability(models.Model):
   hotel_id = models.ForeignKey(hotel,on_delete=models.CASCADE)
   typeofroom = models.CharField(max_length=30)
   date = models.DateField()
   availability = models.IntegerField()
 

class booking(models.Model):
   booking_id=models.AutoField(primary_key=True)
   user_phone= models.ForeignKey(user,on_delete=models.CASCADE)
   checkin = models.DateField()
   checkout = models.DateField()
   no_persons = models.IntegerField()
   hotel_id = models.ForeignKey(hotel,on_delete=models.CASCADE)
   no_rooms = models.IntegerField()





class hotel_login(models.Model):
      hotel_id = models.ForeignKey(hotel,on_delete=models.CASCADE)
      password = models.CharField(max_length=100)






# Create your models here.
