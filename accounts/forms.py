from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model  # 현재 활성화(active)된 user model을 return 하는 함수.

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()  # 유저 모델이 어떤 형태인지 우리는 모른다. 그렇기 때문에 다음의 메서드를 임포트 한다.
        fields = ['email', 'first_name', 'last_name']  # 우리가 원하는 fields만 넣어야 하지만, 우리가 어떻게 알 수 있을까?



# 커스터마이징 한 유저모델을 인식하지 못해서 직접 get_user_model 함수로 유저 모델정보를 넣어준다.
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields