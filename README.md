일단 이렇게 하면 될 겁니다. 

1. 파이썬 가상환경 생성
(pip이 없는 경우에만 > sudo apt install python3-pip)
(venv가 없는 경우에만  > sudo apt install python3-venv)
> python3 -m venv myvenv


2. Virtual Envirionment가 실행
> source myvenv/bin/activate

(myvenv) 가 프롬프트 앞에 붙을것임

3. 가상환경 안에서 패키지 설치 
> pip install -r requirements.txt

4. wifi Analyazer make & venv에 추가
(python 3.6이어야 함. 아니라면 makefile과 wifi_setup.sh 수정 필요)
> source ./withus_wavemon/wifi_setup.sh

5. 장고 서버 실행
>python3 manage.py runserver 0.0.0.0:80
