from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model  # 현재 활성화(active)된 user model을 return 하는 함수.

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()  # 유저 모델이 어떤 형태인지 우리는 모른다. 그렇기 때문에 다음의 메서드를 임포트 한다.
        fields = ['email', 'first_name', 'last_name']  # 우리가 원하는 fields만 넣어야 하지만, 우리가 어떻게 알 수 있을까?