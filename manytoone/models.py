from django.db import models

# Create your models here.
# doctor.patients.all()을 원함.
class Doctor(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{ self.pk } 번 의사 { self.name }'


# patient.doctors.all() 을 원함.
class Patient(models.Model):
    name = models.CharField(max_length=50)
    doctors = models.ManyToManyField(Doctor, related_name='patients')  # 이렇게 하는 순간 patient.doctors.all() 가능 doctor 입장에서는. doctor.patient_set.all()로 접근할 수 있다.
    # 그래서 related_name을 부여한다. 즉, doctor가 입장에서 patients 모두 뽑고 싶을 때, related_name으로 제어할 수 있다. 이러면 reservation table을 생성 할 필요가 없다.
    def __str__(self):
        return f'{ self.pk } 번 환자 { self. name }'


'''
doctor1 = Doctor.objects.create(name='scarlet')
doctor2 = Doctor.objects.create(name='bae')

patient1 = Patient.objects.create(name='Jason', doctor=doctor1)
patient2 = Patient.objects.create(name='Jeong', doctor=doctor2)
patient3 = Patient.objects.create(name='Jeong', doctor=doctor1)  # 닥터2에게 진료받던 정이는 닥터2가 맘에 안들어서, 닥터1에게 다시감... 하지만 이런식으로는 

'''

# class Reservation(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.pk} 번째 진료는 {self.patient.id} 번째 환자({self.patient})가 {self.doctor.id}번 의사({self.doctor}) 에게 받는다.'


'''
doctor1 = Doctor.objects.create(name='Justin')
patient1 = Patient.objects.create(name='Jason')
doctor2 = Doctor.objects.create(name='Django')
patient2 = Patient.objects.create(name='Eunsung')
reservation1 = Reservation.objects.create(patient=patient1, doctor=doctor1)
reservation2 = Reservation.objects.create(patient=patient1, doctor=doctor2)
reservation3 = Reservation.objects.create(patient=patient2, doctor=doctor2)

doctor2.reservation_set.all()
'''

'''
doctor1 = Doctor.objects.create(name='Justin')
patient1 = Patient.objects.create(name='Jason')

등록하는 법
doctor1.patients.add(patient1)  # 1번 의사에게 1번 환자를 추가하는 것

doctor1.patients.all()
patient1.doctors.all()

삭제하기(예약취소)
patient1.doctors.remove(doctor1)

이 기능을 좋아요 기능으로 구현할 것이다.
'''

