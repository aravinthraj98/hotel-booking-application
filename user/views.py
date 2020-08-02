from django.shortcuts import render
from django.http import HttpResponse
from user.models import user,availability,hotel,booking,hotel_login,hotel_type
import datetime
from django.contrib.auth.hashers import make_password,check_password
from datetime import date,timedelta
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
mydate = datetime.datetime.now()
DATE=date.today()
print(mydate)
print(DATE)

def users(request):
    if request.method=='POST':
        log_sign=request.POST['user']
        if log_sign=='signup':
             username=request.POST['username']
        
             password=request.POST['password']
             cpassword=request.POST['cpassword']
             if not len(password)>=8 and password==cpassword:
                 return render(request,'user/show.html',{'msg':'password must be in length of 8 or password and confirm password mus be same'})
             phonenumber=request.POST['phone']
             if not len(username)>=3 and phonenumber.isnumeric() and len(phonenumber)==10:
                    return render(request,'user/show.html',{'msg':'username or phonenumber not in format'})

         
             pass_e=make_password(password)
             print(pass_e)
             if not user.objects.filter(phonenumber=phonenumber).exists():
                 user.objects.create(username=username,password=pass_e,phonenumber=phonenumber)
                 return render(request,'user/show.html',{'msg':'registered successfully'})

             else:
                
                 return render(request,'user/sign.html',{'msg':'phonenumber already exist','user':username,'a':'sign','b':'login'})
        else:
            phonenumber=request.POST['phone']
            login=False
            password=request.POST['password']
            check_p=user.objects.filter(phonenumber=phonenumber)
            for i in check_p:
                if check_password(password,i.password)==True:
                      print('hello')
                      login=True
                      break
                    

            
            if  login==True:
                    response= render(request,'user/show.html')
                    response.set_cookie('user',phonenumber)
                    return response
                   
            else:
                    return render(request,'user/sign.html',{'msg':'phonenumber or password not valid','phone':phonenumber,'a':'login','b':'sign'})
    else:
        return render(request,'user/sign.html')
def hotels(request):
    if request.method=='POST':
        log_sign=request.POST['user']
        if log_sign=='signup':
             hotelname=request.POST['hotelname']
             h_name=hotelname[0:4]
             hotelid=h_name+'-'+get_random_string(3)
             password=request.POST['password']
             phonenumber=request.POST['phone']
             cpassword=request.POST['cpassword']
             if not len(hotelname)>=4 and len(password)>7 and phonenumber.isnumeric() and password==cpassword:
                 return render(request,'user/hotel_sign.html',{'msg':'some field are empty or not in correct format'})
    
            #  fs = FileSystemStorage()
            #  name=fs.save(img.name, img)
            #  url=fs.url(name)
            #  if not url.endswith('jpg' or 'jpeg' or 'png'):
            #             return render(request,'user/hotel_sign.html',{'msg':'file type must be jpg,jpeg'})


             location=request.POST['location']
            #  totalroom=request.POST['totalroom']
             if not len(password)>=8 and password==cpassword:
                 return render(request,'user/show.html',{'msg':'password must be in length of 8 or password and confirm password mus be same'})
             phonenumber=request.POST['phone']
             if not len(hotelname)>=3 and phonenumber.isnumeric() and len(phonenumber)==10:
                    return render(request,'user/show.html',{'msg':'hotel  name or phonenumber not in format'})

             pass_e=make_password(password)
             if hotel.objects.filter(phonenumber=phonenumber).exists():
                      return render(request,'user/hotel_sign.html',{'msg':'your phonenumber already  exist'})
             else:
                 hotel_pass=hotel.objects.create(hotel_id=hotelid,hotel_name=hotelname,phonenumber=phonenumber,hotel_location=location)
                 pass_h=make_password(password)
                 test=hotel_login.objects.create(hotel_id=hotel_pass,password=pass_h)
                 if hotel_login.objects.filter(hotel_id=hotelid,password=password).exists:
                             return render(request,'user/hotel_sign.html',{'msg':'success'})
        else:
                hotel_id=request.POST['hotel_id']
                password=request.POST['password']
                hotel_ids= hotel.objects.filter(hotel_id=hotel_id)
                for i in hotel_ids:
                    id=i
                    break
                validate=hotel_login.objects.filter(hotel_id=id)
                h_login=False
                for i in validate:
                    if check_password(password,i.password)==True:
                        h_login=True
                        break
                if h_login==True:
                    return render(request,'user/admin.html')
                else:
                    return render(request,'user/hotel_sign.html',{'msg':'login credential not MATCHED'})



             

    else:
         return render(request,'user/hotel_sign.html')

def show(request):
        
        if not request.COOKIES.get('user'):
            return render(request,'user/sign.html')

        hotels=hotel.objects.all()
        location=[]
        for i in hotels:
            location.append(i.hotel_location)
        locations=set(location)
        if request.method=="POST":
            location_u = request.POST['location']
            checkin = request.POST['checkin']
            checkout = request.POST['checkout']
            room = request.POST['room_needed']
            dates = date.fromisoformat(checkin)
            dates1 = date.fromisoformat(checkout)
            sub=dates1-dates
            v=str(sub)
            loc_match=hotel.objects.filter(hotel_location=location_u)
            check_avail=[]
            for i in range(int(v[0])):
                date_check=dates+timedelta(i)
                check_avail.append(str(date_check))
           
            match_id=[]

            for q in loc_match:
                        find_hotel=hotel_type.objects.filter(hotel_id=q)
                        print(len(find_hotel))
                        for i in find_hotel:
                                    available=True
                                    if(len(check_avail)>0):
                                        for k in check_avail:
                                            id_match=availability.objects.filter(hotel_id=i.hotel_id,typeofroom=i.typeofroom,date=date.fromisoformat(k))
                                            print('already')
                                            for l in id_match:
                                                if(l.availability<int(room)):
                                                            available=False
                                                            break
                                            if(available==False):
                                                break
                                            if(len(id_match)<1):
                                               
                                                availability.objects.create(hotel_id=q,availability=i.hotel_room,typeofroom=i.typeofroom,date=date.fromisoformat(k))
                                                id_match=availability.objects.filter(hotel_id=i.hotel_id,typeofroom=i.typeofroom,availability__gte=int(room),date=date.fromisoformat(k))

                                            if(id_match):
                                                for j in id_match:
                                                    m=[j.hotel_id,j.typeofroom]
                                                    if not m in match_id:
                                                       match_id.append(m)
                                                    
                        h_id=[]
                        for i in match_id:
                                
                                j=hotel_type.objects.filter(hotel_id=i[0],typeofroom=i[1])
                                for find in j:
                                    dict1={}
                                    print(str(find.hotel_id)+'gg')
                                    k=find.hotel_id
                                    print(k.hotel_id)
                                    dict1['hotel_id']=k.hotel_id
                                    dict1['hotel_price']=find.hotel_price
                                    dict1['checkin']=checkin
                                    dict1['checkout']=checkout
                                    dict1['room']=room
                                    dict1['typeofroom']=find.typeofroom    
                                    dict1['days']=len(check_avail)
                                    h_id.append(dict1)
                        return render(request,'user/show.html',{"hotel":h_id,"location":locations,'checkin':checkin,'checkout':checkout})

                    

                        
                        


                        


        return render(request,'user/show.html',{"hotels":hotels,"location":locations})

def book(request):
    if request.method=='POST':
       
        hotel_id=request.POST['hotel_id']
        room=request.POST['room']
        days=request.POST['days']
        checkin=request.POST['checkin']
        typeofroom=request.POST['type']
        print(hotel_id)
        booked=False
        for i in range(int(days)):
             check=date.fromisoformat(checkin)+timedelta(i)
             avail_find=availability.objects.filter(hotel_id=hotel_id,date=check,typeofroom=typeofroom)

             for i in avail_find:
                if i.availability>=int(room):
                    availability.objects.filter(hotel_id=hotel_id,date=check,typeofroom=typeofroom).update(availability=i.availability-int(room))
                else:
                    booked=True
                    break
             if booked==True:
                 return render(request,'user/show.html',{'msg':'sry this rooms are booked so fast'})
                 break
        if booked==False:
              phone=int(request.COOKIES['user'])
              user_phone=user.objects.filter(phonenumber=phone)
              hotel_id=hotel.objects.filter(hotel_id=hotel_id)
              for i in user_phone:
                  user_phone=i
                  break
              for i in hotel_id:
                  hotel_id=i
                  break
              booking.objects.create(user_phone=user_phone,checkin=checkin,checkout=check,no_persons=int(room)*3,hotel_id=hotel_id,no_rooms=room)
              return render(request,'user/show.html', {'msg':'booking confirm'})

def room_update(request):
    if request.method=='POST':
          room=request.POST['room']
          hotel_id=hotel.objects.filter(hotel_id='raj-123')
          for i in hotel_id:
              hotel_ids=i
              break
          typeofroom=request.POST['type']
          cost=request.POST['price']
          if room=='cost':
             
              if not len(typeofroom)>2 and isnumeric(cost):
                   return render(request,'user/admin.html', {'msg':'booking confirm'})
              
              print(typeofroom)
            
              hotel_type.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom).update(hotel_price=int(cost))
           
              return render(request,'user/admin.html', {'msg':' confirmed'})
          elif room=='vacancy':
              vdate=request.POST['dates']
              vacancy=request.POST['vacancy']
              print(vdate)
              if  availability.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom,date=vdate).exists():
                    availability.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom,date=date.fromisoformat(vdate)).update(availability=vacancy)
              else:
                  print(hotel_id)
                  availability.objects.create(hotel_id=hotel_ids,typeofroom=typeofroom,date=vdate,availability=vacancy)
              return render(request,'user/admin.html', {'msg':' vac'})
          else:
             img=request.FILES['img']
             fs = FileSystemStorage()
             name=fs.save(img.name, img)
             url=fs.url(name)
             if not url.endswith('jpg' or 'jpeg' or 'png'):
                        return render(request,'user/hotel_sign.html',{'msg':'file type must be jpg,jpeg'})
             hotel_type.objects.create(hotel_id=hotel_ids,hotel_room=10,hotel_price=cost,typeofroom=typeofroom,img=url)
             return render(request,'user/admin.html', {'msg':'vacqq'})

              

    else:
        return render(request,'user/admin.html', {'msg':'booking confirm'})

               
               





# Create your views here.

# Create your views here.
