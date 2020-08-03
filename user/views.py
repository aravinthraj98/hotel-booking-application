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
        hotels=hotel.objects.all()
        location=[]
        for i in hotels:
            location.append(i.hotel_location)
        locations=set(location)
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
            
             if not user.objects.filter(phonenumber=phonenumber).exists():
                 user.objects.create(username=username,password=pass_e,phonenumber=phonenumber)

                 response=  render(request,'user/show.html',{'msg':'registered successfully','location':locations})
                 response.set_cookie('user',phonenumber)
                 return response
                 
                

             else:
                
                 return render(request,'user/sign.html',{'msg':'phonenumber already exist','user':username})
        else:
            phonenumber=request.POST['phone']
            login=False
            password=request.POST['password']
            check_p=user.objects.filter(phonenumber=phonenumber)
            for i in check_p:
                if check_password(password,i.password)==True:
                    
                      login=True
                      break
                    

            
            if  login==True:
                    response= render(request,'user/show.html',{'phone':phonenumber,'location':locations})
                    response.set_cookie('user',phonenumber)
                    return response
                   
            else:
                    return render(request,'user/sign.html',{'msg':'phonenumber or password not valid','phone':phonenumber})
    else:
        return render(request,'user/sign.html')
def hotels(request):
    if request.COOKIES.get('hotel'):
        return render(request,'user/admin.html')
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
    
          


             location=request.POST['location']
        
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
                             return render(request,'user/hotel_sign.html',{'msg':hotelid+' is your id registered successful make sure you note it for login credentials'})
        else:
                validate=''
                hotel_id=request.POST['hotel_id']
                password=request.POST['password']
                hotel_ids= hotel.objects.filter(hotel_id=hotel_id)
                for i in hotel_ids:
                    validate=hotel_login.objects.filter(hotel_id=i)
                    break
                
                h_login=False
                for i in validate:
                    if check_password(password,i.password)==True:
                        h_login=True
                        break
                if h_login==True:

                    response=render(request,'user/admin.html')
                    response.set_cookie('hotel',hotel_id)
                    return response
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
            adult=request.POST['adult']
            children=request.POST['children']
            if int(adult)/2>int(children):
                if not int(room)>=int(adult)/2:
                    return render(request,'user/show.html',{'msg':'make sure to choose enough rooms','location':locations})
            else:
                if not int(room)>=(int(adult)+int(children))/3:
                     return render(request,'user/show.html',{'msg':'make sure to choose enough rooms','location':locations})

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
                                   
                                    k=find.hotel_id
                                  
                                    dict1['hotel_id']=k.hotel_id
                                    dict1['hotel_name']=k.hotel_name
                                    dict1['hotel_price']=find.hotel_price
                                    dict1['checkin']=checkin
                                    dict1['checkout']=checkout
                                    dict1['room']=room
                                    dict1['img']=find.img
                                    dict1['typeofroom']=find.typeofroom    
                                    dict1['days']=len(check_avail)
                                    h_id.append(dict1)
                        return render(request,'user/show.html',{"hotel":h_id,"location":locations,'checkin':checkin,'checkout':checkout})

                    

                        
                        


                        


        return render(request,'user/show.html',{"hotels":hotels,"location":locations})

def book(request):
    if not request.COOKIES.get('user'):
            return render(request,'user/sign.html')
    if request.method=='POST':
        hotels=hotel.objects.all()
        location=[]
        for i in hotels:
            location.append(i.hotel_location)
        locations=set(location)
        
       
        hotel_id=request.POST['hotel_id']
        room=request.POST['room']
       
        days=request.POST['days']
        checkin=request.POST['checkin']
        checkout=request.POST['checkout']
        typeofroom=request.POST['type']
        hotel_ide=hotel.objects.filter(hotel_id=hotel_id)
        booked=False
        for i in range(int(days)):
             check=date.fromisoformat(checkin)+timedelta(i)
            
            
             for i in hotel_ide:
                 avail_find=availability.objects.filter(hotel_id=i,date=check,typeofroom=typeofroom)
                 for i in avail_find:
                    if i.availability>=int(room):
                        avails=int(i.availability)-int(room)
                      
                    
                        availability.objects.filter(hotel_id=hotel_id,date=check,typeofroom=typeofroom).update(availability=avails)
                    else:
                        booked=True
                        break
             
             if booked==True:
                 return render(request,'user/show.html',{'msg':'sry this rooms are booked so fast','location':locations})
                 break
        if booked==False:
              phone=int(request.COOKIES['user'])
              user_phone=user.objects.filter(phonenumber=phone)
              hotel_id=hotel.objects.filter(hotel_id=hotel_id)
              for i in user_phone:
                  user_phone=i
                  break
              
              for i in hotel_id:
                 booking.objects.create(user_phone=user_phone,checkin=checkin,checkout=date.fromisoformat(checkout),no_persons=int(room)*3,hotel_id=i,no_rooms=room)
                 return render(request,'user/show.html', {'msg':'booking confirmed','location':locations})
                 break
            
              return render(request,'user/show.html', {'msg':'some error occured','location':locations})

def room_update(request):
    if not request.COOKIES.get('hotel'):
            return render(request,'user/hotel_sign.html')
    if request.method=='POST':
          room=request.POST['room']
          hotel_id=hotel.objects.filter(hotel_id=request.COOKIES['hotel'])
          for i in hotel_id:
              hotel_ids=i
              break
          typeofroom=request.POST['type']
         
          cost=request.POST['price']
          if room=='cost':
              if not hotel_type.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom).exists():
                   return render(request,'user/admin.html', {'msg':'room type not exist'})
          
              if not len(typeofroom)>2 and cost.isnumeric():
                   return render(request,'user/admin.html', {'msg':'some fields are not valid'})
              
            
            
              hotel_type.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom).update(hotel_price=int(cost))
           
              return render(request,'user/admin.html', {'msg':' confirmed'})
          elif room=='vacancy':
              vdate=request.POST['dates']
              vacancy=request.POST['vacancy']
              
              if  availability.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom,date=vdate).exists():
                    availability.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom,date=date.fromisoformat(vdate)).update(availability=vacancy)
              else:
                  availability.objects.create(hotel_id=hotel_ids,typeofroom=typeofroom,date=vdate,availability=vacancy)
              return render(request,'user/admin.html', {'msg':' availability updated'})
          else:
             img=request.FILES['img']
             fs = FileSystemStorage()
             name=fs.save(img.name, img)
             url=fs.url(name)
             if not url.endswith('jpg' or 'jpeg' or 'png'):
                        return render(request,'user/hotel_sign.html',{'msg':'file type must be jpg,jpeg'})
             if  hotel_type.objects.filter(hotel_id=hotel_ids,typeofroom=typeofroom).exists():
                 return render(request,'user/admin.html', {'msg':'this catagory already exist'})
             hotel_type.objects.create(hotel_id=hotel_ids,hotel_room=10,hotel_price=cost,typeofroom=typeofroom,img=url)
             return render(request,'user/admin.html', {'msg':'new catagory added'})

              

    else:
        return render(request,'user/admin.html')
def detail(request):
    if not request.COOKIES.get('hotel'):
        return render(request,'user/hotel_sign.html')
    if request.method=='POST':
        hotel_id=hotel.objects.filter(hotel_id=request.COOKIES['hotel'])
        for i in hotel_id:
            hotel_ids=i
            break
        detail=request.POST['detail']
      
        if detail=='availability':
            availablity_detail=[]
            avail_detail=availability.objects.filter(hotel_id=hotel_ids)
            for i in avail_detail:
                dict2={}
                dict2['typeofroom']=i.typeofroom
                dict2['date']=i.date
                dict2['availability']=i.availability
                print(i.availability)
                availablity_detail.append(dict2)
            if len(avail_detail)==0:
                 return render(request,'user/detail.html',{'a_detail':avail_detail,'msg':'nothing to show'})


            return render(request,'user/detail.html',{'a_detail':availablity_detail})
        elif detail=='bookings':
            booking_detail=[]
            book_detail=booking.objects.filter(hotel_id=hotel_ids)
            for i in book_detail:
                dict2={}
                dict2['phone']=i.user_phone
                dict2['checkin']=i.checkin
                dict2['checkout']=i.checkout
                dict2['maxperson']=i.no_persons
                dict2['noofrooms']=i.no_rooms
                booking_detail.append(dict2)
            if len(book_detail)==0:
                return render(request,'user/detail.html',{'b_detail':booking_detail,'msg':'no booking available'})

            return render(request,'user/detail.html',{'b_detail':booking_detail})
        else:
            catagory_detail=[]
            cata_detail=hotel_type.objects.filter(hotel_id=hotel_ids)
            for i in cata_detail:
                dict2={}
                dict2['typeofroom']=i.typeofroom
                dict2['noofrooms']=i.hotel_room
                print(i.hotel_room)
                dict2['price']=i.hotel_price
                catagory_detail.append(dict2)
            if len(cata_detail)==0:
                 return render(request,'user/detail.html',{'c_detail':catagory_detail,'msg':'nothing to show'})

                
            return render(request,'user/detail.html',{'c_detail':catagory_detail})
    else:
            return render(request,'user/detail.html')

            

            
            



def logout(request):
    if request.COOKIES.get('user'):
          response= render(request,'user/sign.html')
          response.delete_cookie('user')
          return response
    elif request.COOKIES.get('hotel'):
          response= render(request,'user/hotel_sign.html')
          response.delete_cookie('hotel')
          return response
               
               





# Create your views here.

# Create your views here.
