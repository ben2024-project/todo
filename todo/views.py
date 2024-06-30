from django.shortcuts import render,redirect

from django.views.generic import View

from todo.models import Task

from todo.forms import TaskForm,RegistrationForm,LoginForm

from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from todo.decorators import signin_required

from django.utils.decorators import method_decorator


@method_decorator(signin_required,name="dispatch")
class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()
        
        qs=Task.objects.filter(user_object=request.user)

        return render(request,"task_add.html",{"form":form_instance,"data": qs})


    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=request.user

            form_instance.save()

            messages.success(request,"Task created")

            return redirect("task-add")
        
        else:

            messages.error(request,"Faild")

            return render(request,"task_add.html",{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")
class TaskUpdateView(View):

     def get(self,request,*args,**kwargs):
         
        id=kwargs.get("pk")

        task_object=Task.objects.get(id=id)
     
        form_instance=TaskForm(instance=task_object)

        return render(request,"task_edit.html",{"form":form_instance})
     
     def post(self,request,*args,**kwargs): 
    
         id=kwargs.get("pk")

         task_object=Task.objects.get(id=id)

         form_instance=TaskForm(instance=task_object,data=request.POST)

         if form_instance.is_valid():
              
              form_instance.save()

              messages.success(request,"Task changed")

              return redirect("task-add")
         else:
              
               messages.error(request,"Faild")
              
               return render(request,"task_edit.html",{"form":form_instance})
         

@method_decorator(signin_required,name="dispatch")
class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        qs = Task.objects.get(id=id)

        return render(request,"task_detail.html",{"data":qs})     


@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Task.objects.get(id=id).delete()

        messages.success(request,"Task removed")

        return redirect("task-add")       
    

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"registration.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            print("user object created")

            return redirect("signin")
        
        else:

            print("failed")

            return render(request,"registration.html",{"form":form_instance})
        
class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})     
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("dashboard")
            
        messages.error(request,"Invalid User")    
            
        return render(request,"login.html",{"form":form_instance})   

@method_decorator(signin_required,name="dispatch")    
class SignOutView(View):

     def get(self,request,*args,**kwargs):

         logout(request)

         return redirect("signin") 
       

@method_decorator(signin_required,name="dispatch")
class DashboardView(View):

     def get(self,request,*args,**kwargs):
         
         qs=Task.objects.filter(user_object=request.user)
         
         return render(request,"dashboard.html",{"data":qs})
      

     









                      