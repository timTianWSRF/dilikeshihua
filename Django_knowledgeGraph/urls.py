"""Django_knowledgeGraph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from KG import views
from django.template import loader,RequestContext

urlpatterns = [
    # 子路由添加
    # html界面路由
    url(r'^admin', admin.site.urls),
    url(r'^adata', views.adata),
    url(r'^add_stu/$', views.main, name='add_stu'),
    url(r'^select/$', views.home, name='select'),
    url(r'^database', views.datapage),
    url(r'^draw_geo', views.draw_geo),
    url(r'^tmp', views.draw_map),
    url(r'^edit', views.edit),
    url(r'^PathResult', views.PathResult),

    # ajax传参路由
    url('classfiy$', views.classfiy),
    url('tablecol$', views.tablecol),
    url('getdocumentname$', views.getdocumentname),
    url('path$', views.path),
    url('setele$', views.setele),
    url('data$', views.data),
    url('aim1$', views.aim1, name="aim"),
    url('add$', views.add),
    url('delete$', views.delete),
    url('update$', views.updata),
    url('addpagecol$', views.addpagecol),
    url(r'^add_stu/aim.txt/$', views.aim),
    url(r'^select/aim.txt/$', views.aim),
    url(r'^logout1/aim.txt/$', views.aim),
    url(r'^logout2/aim.txt/$', views.aim),
    url(r'^database/$', views.render_database, name="database"),
    # url(r'^select/database/', views.render_database),
    # url(r'^logout1/database/', views.render_database),
    # url(r'^logout2/database/', views.render_database),
    url(r'^$', views.login2, name='login'),
    url(r'^login/$', views.login2, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^test/$', views.test, name='get_cookie'),
    url(r'^logout1/$', views.logout1),
    url(r'^logout2/$', views.logout2),
    url(r'^geo/$', views.geo, name="geo"),
    url(r'^temp/$', views.temp, name="temp"),
    url(r'^findroad/$', views.find_road, name="find_road"),
    url(r'^kmeans/$', views.web_k_means, name="k_means"),
    url(r'^kmeanside/$', views.web_inside_k_means, name="KMEANS"),
    url(r'^pleaselogin/$', views.please_login, name="pleaselogin"),
    url(r'^heatmap/$', views.heat_map, name="heat_map"),
    url(r'^insideheatmap/$', views.inside_heat_map, name="inside_heat_map"),
    url(r'^summarize/$', views.summarize, name="summarize"),
    url(r'^fuzhujuece/$', views.fuzhujuece, name="fuzhujuece"),
    url(r'^fzjc/$', views.fzjc, name="fzjc"),



    # url(r'^tablea', views.datapage),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

