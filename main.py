import cv2
import aircv as ac
import os
from PIL import Image
from PIL import ImageGrab
import time
import datetime

#改变图片分辨率（因为手机图片发送到电脑截图与原分辨率不同）
def resize_image(input_image,out_image,width,height,type):
    img = Image.open(input_image)
    out_rule = img.resize((width,height),Image.ANTIALIAS)
    out_rule.save(out_image,type)


#从手机截屏，并发送到电脑
#新方案，电脑安装投影软件，更快
def get_now_picture():
    os.popen("adb shell screencap -p /sdcard/screen.png")
    os.popen("adb pull /sdcard/screen.png")
    #改变图片分辨率
    resize_image('screen.png','screen_out.png',430,760,'png')

#    bbox = (10, 60, 525, 990)
#    img = ImageGrab.grab(bbox)
#    img.save("D:/lu-tool/script/python/test/begain/screen_out.png")

#获取手机需要被点击的点(返回为需要点击的手机坐标的高宽数组)
def get_phone_point(pos):
    #手机分辨率与图片分辨率，如更改，需修改
    phone_heigh = 1920.0
    phone_width = 1080.0
    picture_height = 760
    picture_width = 430
    resolution_list = []
    
    #获取匹配出的中心点
    point = pos['result']
    get_height = point[1]
    get_width = point[0]
    #将图片点坐标转换为手机对应坐标
    phone_point_height = phone_heigh/picture_height*get_height
    phone_point_width = phone_width/picture_width*get_width
    resolution_list.append(phone_point_height)
    resolution_list.append(phone_point_width)
    return resolution_list


#打开两个图片进行匹配（返回为匹配出点的信息）
def compare(source_picture,goal):
    imsrc = ac.imread(source_picture)
    imobj = ac.imread(goal)    
#    imsrc = cv2.imread(source_picture)
#    imobj = cv2.imread(goal)
    pos = ac.find_template(imsrc, imobj)
    
    return pos


#对手机进行操作
def phone_handle(handle,argument):
    if handle == "click":
        os.popen("adb shell input tap {x} {y}".format(x=argument[1],y=argument[0]) )
    elif handle == 'insert':
        num_arry=[7,8,9,10,11,12,13,14,15,16]
        argu_leng = len(argument)
        for num in range(argu_leng):
            send_num = int(argument[num])            
            os.popen('adb shell input keyevent {date}'.format(date=num_arry[send_num]))
        
    

def draw_circle(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('objDetect', imsrc) 
    cv2.waitKey(1)
    cv2.destroyAllWindows()


#打开图片并关闭，目的是为了关闭图像流，这个坑爹的作者仿佛没有写关闭图像的接口，
#导致读取第一张图后后面的也全部与第一张图片匹配
def close_picture(pictur_name):
    imsrc = ac.imread(pictur_name)
    cv2.imshow('objDetect', imsrc) 
    cv2.waitKey(1)
    cv2.destroyAllWindows()




if __name__ == "__main__":
  total=10
  for  num in range(191,300) :
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#从手机获取当前图片
    get_now_picture()
    
#图片进行比较（第一个参数为手机截屏，第二个参数为需要对比的图片）
    pos = compare('screen_out.png','+.png')

#获取目标点(返回为高宽的数组)
    #如果手机分辨率改变，需要更改此函数里面的手机分辨率参数
    phone_point = get_phone_point(pos)

#对手机进行操作
    phone_handle("click",phone_point)

#关闭图像流，否则读取第一张图后后面的也全部与第一张图片匹配
    close_picture('screen_out.png')
    close_picture('+.png')
    print "+ over"
    time.sleep(2)


    get_now_picture()
    pos = compare('screen_out.png','make.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('make.png')
    print "make over"
    time.sleep(2)

    get_now_picture()
    pos = compare('screen_out.png','delete.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('delete.png')
    print "delete over"

    get_now_picture()
    pos = compare('screen_out.png','name.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    name_num = str(num)
    phone_handle("insert",name_num)
    print name_num
    close_picture('screen_out.png')
    close_picture('name.png')
    print "name over"

    get_now_picture()    
    pos = compare('screen_out.png','inputdown.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('log.png')
    print "imputdown over"


    pos = compare('screen_out.png','log.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('log.png')
    print "logo over"

    get_now_picture() 
    pos = compare('screen_out.png','begin_make.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('log.png')
    print "begin_make over"
    time.sleep(8)

#    get_now_picture()    
#    pos = compare('screen_out.png','input_cheke.png')
#    phone_point = get_phone_point(pos)
#    phone_handle("click",phone_point)
#    close_picture('screen_out.png')
#    close_picture('log.png')
#    print "input_cheke over"


#    get_now_picture()
#    pos = compare('screen_out.png','cheke.png')
#    phone_point = get_phone_point(pos)
    phone_check = '5664968'
    phone_handle("insert",phone_check)
    close_picture('screen_out.png')
    close_picture('make.png')
    print "check(only this phone) over"
    time.sleep(1)

    get_now_picture()
    pos = compare('screen_out.png','check_install.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('log.png')
    print "check_install over"
    time.sleep(13)


    get_now_picture() 
    pos = compare('screen_out.png','install.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('log.png')
    print "install over"    
    time.sleep(10)


    get_now_picture() 
    pos = compare('screen_out.png','complete.png')
    phone_point = get_phone_point(pos)
    phone_handle("click",phone_point)
    close_picture('screen_out.png')
    close_picture('log.png')
    print "complete over"
    time.sleep(3)

