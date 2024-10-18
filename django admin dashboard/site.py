
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.urls import path
from django.apps import apps
from django.contrib.auth import logout as LogOutFunction
from .forms import GlobalForms
from django.contrib import messages
from django.db.models import Q
class Site:
    # Text to put at the end of each page's <title>.
    site_logo= "BinuRice"
    # Text to put in each page's <div id="site-name">.
    site_header =  "BinuRice Admin Is comming"
    # Text to put at the top of the admin index page.
    logout_url = "logout"
    ViewSite_Url = None
    def __init__(self):
        self._registry = {}
        self.action = {}

    def globalContext(self,request):
        if request.user.is_active and request.user.is_staff:
            return {
                "logo":self.site_logo,
                "site_title":self.site_header,
                "logout_url":self.logout_url,
                "view_site":self.ViewSite_Url,
                "has_permission":self.has_permission(request),
            }
    
    def logout(self,request):
        if request.user.is_active and request.user.is_staff:
                
            LogOutFunction(request)
            return redirect("home")
        else:
            return HttpResponse("error")
   
    def has_permission(self,request):
        return request.user.is_active and request.user.is_staff

    def index(self,request):
        if request.user.is_active and request.user.is_staff:
            all_posts = [self.FindModelByClass(all_models).__name__ for all_models,childModel in self._registry.items() if self.FindModelByClass(all_models) and self._registry]
            if "model" in self.action  and "slug" in self.action:
                self.action.pop("slug")
            return render(request, "django-admin/index.html",context={
                **self.globalContext(request),
                "models":all_posts,
                
            })
        else:
            return HttpResponse("You do not have permission. ❌",status=403)
    
    def CheckModelHisRelatedModels(self,model):
        UpdatedIs = []
        if self._registry:
            for m , childs in self._registry.items():
                if model.lower()==m.lower() and m and model:
                    UpdatedIs =  list(childs["related"])
                    UpdatedIs.append(m)
                    if "action" in childs and childs["action"]:
                        self.action["model"] = m
                        self.action["action"]= childs["action"] 
                        self.action["related"] = childs["related"] 
                    return UpdatedIs
                if childs and not m==model:
                    for child in childs["related"]:
                        if child == model:
                            UpdatedIs= list(childs["related"])
                            UpdatedIs.append(m)
                            return UpdatedIs   
        return UpdatedIs

    def DeleteThisModelPost(self,request,model,pk):
        if request.user.is_active and request.user.is_staff:  
            DelteThis = get_object_or_404(self.FindModelByClass(model),id=pk)
            DelteThis.delete()
            messages.success(request,"Item successfully deleted! 😊")
            return redirect("model-view",model=model)
        else:
            return HttpResponse("Access denied! Only staff can delete items. 🚫")
    
    def Update_previus_Model(self,request,model,pk):
        if request.user.is_active and request.user.is_staff:
            focusThisModel = get_object_or_404(self.FindModelByClass(model),id=pk)
            DynamicForm = GlobalForms(self.FindModelByClass(model))
            Form = DynamicForm(instance=focusThisModel)
            if request.method=="POST":
                Form = DynamicForm(data=request.POST,files=request.FILES,instance=focusThisModel)
                if Form.is_valid():
                    Form.save()
                    messages.success(request,"Item updated successfully! ✔️")
                    return redirect("update-past-model",model=model,pk=pk)
                else:
                    messages.error(request,"There were errors in the form. Please correct them. ❌")
            else:

                
                context ={
                    **self.globalContext(request),
                    "form":Form,
                    "model_name":model,
                    "update":True
                }
                if self.CheckModelHisRelatedModels(model):
                    context["models"] =[self.FindModelByClass(m).__name__ for m in self.CheckModelHisRelatedModels(model)]
                else:
                    all_model = [self.FindModelByClass(all_models).__name__ for all_models,childModel in self._registry.items() if self.FindModelByClass(all_models)]
                    context["models"]=all_model
                if "model" in self.action and model == self.action["model"] and "action" in self.action:
                    self.action["slug"] = getattr(focusThisModel,self.action["action"],None)
                return render(request,"global-admin/create_or_update.html",context=context)
        else:
            return HttpResponse("You do not have permission to update this item. ❌")
    
    def RegisterModel(self,model):
        self._registry = model
        return self._registry
    
    def Create_new_Model(self,request,model):
        if request.user.is_active and request.user.is_staff:
            form = GlobalForms(self.FindModelByClass(model))
            if request.method=="POST":
                form = form(data=request.POST,files=request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request,"Item created successfully! ✔️")
                    return redirect("model-view",model=model)
                else:
                    messages.error(request,"There were errors in the form. Please correct them. ❌")
            else:
                context ={
                    **self.globalContext(request),
                    "form":form,
                    "model_name":model
                }
                if self.CheckModelHisRelatedModels(model):
                    context["models"] =[self.FindModelByClass(m).__name__ for m in self.CheckModelHisRelatedModels(model)]
                else:
                    all_model = [self.FindModelByClass(all_models).__name__ for all_models,childModel in self._registry.items() if self.FindModelByClass(all_models)]
                    context["models"]=all_model
                return render(request,"global-admin/create_or_update.html",context=context)
        else:
            return HttpResponse("You do not have permission to Add item. ❌")
    
    def ModelViewByAction(self,request,model):
        if request.user.is_active and request.user.is_staff:
            MyModel = self.FindModelByClass(model)
            if MyModel:
                context={
                    **self.globalContext(request),
                }
                if "related" in self.action and  model in self.action["related"] and "slug" in self.action:
                    checkBYThis = f"post__{self.action['action']}"
                    context["selected_model"] = MyModel.objects.filter(Q(**{checkBYThis:self.action["slug"]})).order_by("id")

                else:
                    context["selected_model"] = MyModel.objects.all().order_by("id")
                context["model_name"]=model
                if self.CheckModelHisRelatedModels(model):
                    context["models"] =[self.FindModelByClass(m).__name__ for m in self.CheckModelHisRelatedModels(model) if self.FindModelByClass(m)]
                else:
                    all_model = [self.FindModelByClass(all_models).__name__ for all_models,childModel in self._registry.items() if self.FindModelByClass(all_models)]
                    context["models"]=all_model
                
                return render(request,"django-admin/model-view.html",context)
            else:
                return HttpResponse(f"404 {model}")
        else:
            return HttpResponse("You do not have permission to Add item. ❌")
        
    def FindModelByClass(self,ModelClassName):
        class_name = ModelClassName  # Replace with your model class name
        model = None

        # Iterate over all installed apps
        for app_config in apps.get_app_configs():
            # Check each model in the app
            for all_model in app_config.get_models():
                if all_model.__name__.lower() == class_name.lower():
                    model = all_model
            if model:
                pass
        return model
    
    def urls(self):
        urlpatterns = [
            path("",self.index,name="home"),
            path("logout",self.logout,name="logout"),
            path("model-view/<str:model>",self.ModelViewByAction,name="model-view"),
            path("create-new-one/<str:model>/",self.Create_new_Model,name="create-new-model"),
            path("update-one/<str:model>/<int:pk>",self.Update_previus_Model,name="update-past-model"),
            path("delete-one/<str:model>/<int:pk>",self.DeleteThisModelPost, name="delete-this-model"),
        ]
        return urlpatterns
admin_site= Site()
urls = admin_site.urls()