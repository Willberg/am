from rest_framework.throttling import SimpleRateThrottle


class VisitThrottle(SimpleRateThrottle):
    # 匿名用户60s只能访问三次（根据ip）
    scope = 'ANONYMOUS'  # 这里面的值，自己随便定义，settings里面根据这个值配置Rate

    def get_cache_key(self, request, view):
        # 通过ip限制节流
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    # 登录用户60s可以访问10次
    scope = 'AUTH'  # 这里面的值，自己随便定义，settings里面根据这个值配置Rate

    def get_cache_key(self, request, view):
        return request.user.username
