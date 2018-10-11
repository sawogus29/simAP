일단 이렇게 하면 될 겁니다. 

1. 파이썬 가상환경 생성
> python3 -m venv myvenv

2. Virtual Envirionment가 실행
> source myvenv/bin/activate

(myvenv) 가 프롬프트 앞에 붙을것임

3. 가상환경 안에서 패키지 설치  
> pip install -r requirements.txt

4. 장고 서버 실행
>python3 manage.py runserver 0.0.0.0:80