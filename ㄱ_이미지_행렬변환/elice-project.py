from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime as dt
import pandas as pd 
import time
import PIL.Image as image
import urllib.request
import cv2
import numpy as np
import sys

import tensorflow as tf


class Album:
    def __init__(self, img, artist, title, time, type):
        self.img = img
        self.artist = artist
        self.title = title
        self.time = time
        self.type = type

url_list = []
url = 'https://music.bugs.co.kr/genre/kpop/indie/total?tabtype=3&sort=default&nation=all&page='
for i in range(1, 92):
    url = url + str(i)
    url_list.append(url)
    url = 'https://music.bugs.co.kr/genre/kpop/indie/total?tabtype=3&sort=default&nation=all&page='
    #print(url_list)


with webdriver.Chrome('chromedriver.exe') as driver:
    driver.get(url_list[90])

    album_list=[]
    # 페이지네이션 구현 못함


    #앨범 이미지
    img_list = []
    thumbnail = driver.find_elements(By.CLASS_NAME, 'thumbnail')
    for i in thumbnail:
        url_list = i.find_elements(By.TAG_NAME, 'img')

        for url in url_list:
            img = url.get_attribute('src')
            img_list.append(img)


    #앨범 정보
    info_list = driver.find_elements(By.CLASS_NAME, 'info')
    for info in info_list:
        artist = info.find_element(By.CLASS_NAME, 'artistTitle').text
        title = info.find_element(By.TAG_NAME, 'a').text
        time = info.find_element(By.TAG_NAME, 'time').text
        type = info.find_element(By.CLASS_NAME, 'albumType').text

        album = Album(img, artist, title, time, type)

        album_list.append(album)


    artist_list = []
    title_list = []
    time_list = []
    type_list = []
    for album in album_list:

        artist_list.append(album.artist)
        title_list.append(album.title)
        time_list.append(album.time)
        type_list.append(album.type)
    
    #print(img_list)
    #print(artist_list)
    #print(title_list[0])
    #print(time_list[0])
    #print(type_list[0])


# 앨범발매일 파생변수 생성
year=[]
month=[]
day=[]
for time in time_list:
    year.append(time[:4])
    month.append(time[5:7])
    day.append(time[8:])
#print(year)
#print(month)
#print(day)


# 데이터프레임 생성
frame = [img_list, artist_list, title_list, time_list, type_list, year, month, day]
df = pd.DataFrame(frame).rename({0:'img_url', 1:'artist', 2:'title', 3:'time', 4:'type', 5:'year', 6:'month', 7:'day'}).T
df = df[df['year']=='2022']  # 2022년 데이터만 사용하기 위해
print(df)


# img_url변수 전처리 
imgurl=[]
imgarr=[]
for url in df['img_url']:
    url = url.split("?")[0]
    imgurl.append(url)
    img = urllib.request.urlretrieve(url, url.split("/")[-1]) #이미지 다운로드
    print('download sucessful')


    # 이미지를 행렬로 만들기
    img2 = cv2.imread(url.split("/")[-1], cv2.IMREAD_COLOR)
    #cv2.imshow('this is album image', img2)
    #cv2.waitKey(0) #이미지를 확인할 수 있는 창이 뜸
    img3 = np.array(img2)
    #print(img3)
    #print(img3.shape) #(170, 170, 3)
    imgarr.append(img3)
#print(imgurl)
#print(imgarr)


# csv 파일로 저장
df['img_url'] = imgurl
df['img_arr'] = imgarr
df.to_csv('elice_project.csv', index=False)
#check = pd.read_csv('elice_project.csv')
#print(check)