from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from crm import models


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in [reverse("crm:login"),reverse("crm:reg")]:
            return None
        if request.path_info.startswith("/admin"):
            return None
        # 没登录，跳转到登录页面
        if not request.session.get("is_login"):
            return redirect(reverse("crm:login"))
        #         登录成功,保存登录的用户对象
        obj = models.UserProfile.objects.filter(pk=request.session.get("user_id")).first()
        if obj:
            # 不要使用request.user，这个变量已经被django自己的auth中间件使用。
            request.user_obj = obj
