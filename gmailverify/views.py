from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from gmailverify.models import Profile
import datetime
import random
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def index(request):
    return HttpResponse("Hello from index file")

def register(request):
#fetch data from POST request 
    if request.method=="POST":
        content={}
        uname=request.POST['umail']
        mb=request.POST['umobile']
        upass=request.POST['upass']
        cpass=request.POST['cpass']
        
        # print(uname)
        # print(mb)
        # print(upass)
        # print(cpass)
        #validation
        if uname=='' or mb=='' or upass=='' or cpass=='':
            content['errmsg']="Field cannot be Empty"
        elif not(mb.isdigit() and len(mb)==10):
            content['errmsg']="Invaild mobile number. It must be 10 digits"                
        elif upass!=cpass:
                content['errmsg']="password and confirmed password didn't match"
        else:
            
            try:
                u=User.objects.create(username=uname,password=upass,email=uname,is_active=1,date_joined=datetime.datetime.now())
                u.set_password(upass)
                u.save()
                
            except Exception:
                content['errmsg']="Username Already Exists!!!"

            try:
                p=Profile.objects.create(uid=u,mobile=mb)
                # print(p)
                p.save()
            except Exception:
                content['errmsg']="Mobile Number Already Exists!!"
            
            if u and p:
                 url='/verifyscreen/'+str(u.id)
                 return redirect(url)
            
        return render(request,'register.html',content)
    else:
        return render(request,'register.html')
        
def user_login(request):
    if request.method=="POST":
        pass
    else:
        return render(request,'login.html')
    
def verifyscreen(request,rid):
    u=User.objects.filter(id=rid)
    r=u[0].email
    otp=str(random.randrange(1000,9999))
    msg="OTP for Email Verification: "+str(otp)
    s="Email verification" 
    request.session[r]=otp
    send_mail(
            s,
            msg,
            settings.EMAIL_HOST_USER,
            [r],
            fail_silently=False,
            )  
    content={}
    content['user_id']=rid
     #store otp in the database
    return render(request,'verifyscreen.html',content)


def verifyotp(request,rid):
    otp=request.POST['uotp']
    u=User.objects.filter(id=rid)
    uemail=u[0].email
    sess_otp=request.session[uemail]
    # print("session otp:",sess_otp)
    # print("User otp:",otp)
    # print("userid:",rid)
    if int(otp)==int(sess_otp):
        return render(request,'gmailsuccess.html')
     