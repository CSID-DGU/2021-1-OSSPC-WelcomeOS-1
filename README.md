# 2021-1-OSSPC-WelcomeOS-1
![Github license](https://img.shields.io/github/license/CSID-DGU/2021-1-OSSPC-WelcomeOS-1)
![badges](https://img.shields.io/badge/OS-ubuntu-red)
![badges](https://img.shields.io/badge/python-3.8-blue)
![badges](https://img.shields.io/badge/pygame-2.0.0-orange)

pygame 활용 테트리스 게임 **"Block King"**  
(original source: [Tetris Kingdom](https://github.com/CSID-DGU/2020-2-OSSP-CP-17woljang-9))

**1조 어서오소**  
**Team Leader**: [주현이](https://github.com/hyeoneedyou)  
**Team Member**: [김현하](https://github.com/kimhyeonhaa), [이채림](https://github.com/leechaelim)

< Tetris Kingdom 2 >

![image](https://user-images.githubusercontent.com/58203135/121075993-d1cf7c80-c810-11eb-8ba6-3a9fe5c4f1e5.png)

## 실행 방법
### 1. Python 3.8 설치
```
$ sudo apt update
$ sudo apt install python3.8
```
### 2. venv(가상환경) 설치

```
$ sudo apt-get install python3.8-venv

```
### 3. 가상환경 생성
먼저, 현재 우리 프로젝트에 접근합니다.
```
$ cd 2021-1-OSSPC-WelcomeOS-1
```
가상환경을 생성합니다.
```
$ python3.8 -m venv myvenv
```
myvenv라는 폴더가 생성됐다면 제대로 생성된 것입니다.

### 4. 가상환경 실행
```
$ source ./myvenv/bin/activate
```
(myvenv)가 표시된다면 가상환경이 잘 실행된 것입니다.
### 5. pygame 2.0.0 설치
```
$ pip3 install pygame==2.0.0
```

