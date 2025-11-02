from flask import Blueprint, render_template, request, jsonify, redirect, flash, url_for
from Core.StudentController import StudentController,DiningInfo
from Core.DishController import DishController
import Core.Statistician as Statistician
from datetime import datetime

'''首页'''
views_bp = Blueprint('views', __name__ ,url_prefix='/views')

def get_dining_time() -> dict:
    '''获取学生就餐时间\n'''
    time = {'早餐':0,'午餐':0,'晚餐':0,'夜宵':0,'其他':0}
    for students in StudentController().get_all_students():
        for dining in students.dining_info_list:
            if 7<=dining.dining_time.hour<9:
                time['早餐'] = time.get('早餐',0) + 1
            elif 12<=dining.dining_time.hour<14:
                time['午餐'] = time.get('午餐',0) + 1
            elif 17<=dining.dining_time.hour<19:
                time['晚餐'] = time.get('晚餐',0) + 1
            elif 22<=dining.dining_time.hour<=23:
                time['夜宵'] = time.get('夜宵',0) + 1
            else:
                time['其他'] = time.get('其他',0) + 1
    # sort_time = sorted(time.items(),key=lambda x:x[1],reverse=True)
    return time

def get_dining_location() -> dict:
    '''统计学生就餐地点次数\n'''
    location = {'北区':0,'南区':0,'堕落街':0,'其他':0}
    for students in StudentController().get_all_students():
        for dining in students.dining_info_list:
            if dining.location == '北区':
                location['北区'] = location.get('北区',0) + 1
            elif dining.location == '南区':
                location['南区'] = location.get('南区',0) + 1
            elif dining.location == '堕落街':
                location['堕落街'] = location.get('堕落街',0) + 1
            else:
                location['其他'] = location.get('其他',0) + 1
    return location

def get_dishes_location() -> dict:
    '''统计菜品就餐地点次数\n'''
    location = {'北区':0,'南区':0,'南堕落街':0, '北堕落街':0 ,'西餐厅':0,'竹韵食堂':0}
    for dish in DishController().get_all_dishes():
        if dish.location == '北区':
            location['北区'] = location.get('北区',0) + 1
        elif dish.location == '南区':
            location['南区'] = location.get('南区',0) + 1
        elif dish.location == '南堕落街':
            location['南堕落街'] = location.get('南堕落街',0) + 1
        elif dish.location == '北堕落街':
            location['北堕落街'] = location.get('北堕落街',0) + 1
        elif dish.location == '西餐厅':
            location['西餐厅'] = location.get('西餐厅',0) + 1
        elif dish.location == '竹韵食堂':
            location['竹韵食堂'] = location.get('竹韵食堂',0) + 1
        else:
            location['其他'] = location.get('其他',0) + 1
    return location


@views_bp.route('/index', methods=['GET','POST'])
def index():
    now = datetime.now() # 获取当前时间
    format_now = now.strftime('%Y-%m-%d %H:%M:%S') # 格式化时间

    len_stu = len(StudentController().get_all_students()) # 获取学生数量
    len_dish = len(DishController().get_all_dishes()) # 获取菜品数量

    dish_counts = Statistician.Statistician(StudentController()).get_dish_counts(5) # 获取菜品数量
    dish_labels = [labels for labels in dish_counts.keys()] # 菜品名称
    dish_num = [number for number in dish_counts.values()]  # 菜品数量

    time_labels = [labels for labels in get_dining_time().keys()] # 就餐时间标题
    time_num = [number for number in get_dining_time().values()] # 就餐时间数量

    location_labels = [labels for labels in get_dining_location().keys()] # 就餐地点标题
    location_num = [number for number in get_dining_location().values()]  # 就餐地点数量

    location_dishes_labels = [labels for labels in get_dishes_location().keys()] # 菜品就餐地点标题
    location_dishes_num = [number for number in get_dishes_location().values()] # 菜品就餐地点数量

    return render_template('index.html',  format_now=format_now, all_dishes = sum(location_dishes_num), 
                            len_stu=len_stu, len_dish=len_dish, 
                            labels=dish_labels, datas=dish_num,
                            time_labels=time_labels, time_num=time_num,
                            location_labels=location_labels, location_num=location_num,
                            location_dishes_labels=location_dishes_labels, location_dishes_num=location_dishes_num)