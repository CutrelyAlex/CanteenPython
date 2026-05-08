from typing import List, Dict, Any
from datetime import datetime

from Core.DishModel import Dish
from Core.json_storage import load_json_list, save_json_list

class DiningInfo:
    '''就餐信息类'''
    def __init__(self, dining_time: datetime, dishes: List[str], remarks: str, location: str = "Unknown", images: List[str] = None):
        '''
        初始化 DiningInfo 对象
        参数:
            dining_time: 就餐时间 datetime
            dishes: 对应菜品名称列表 List[str]
            remarks: 备注 str
            location: 就餐位置 str (默认 "Unknown")
            images: 就餐后照片列表 List[str] (默认空列表)
        '''
        self.dining_time = dining_time
        self.dishes = dishes
        self.remarks = remarks
        self.location = location
        self.images = images if images is not None else []

class PersonalProfile:
    '''个人简介类'''
    def __init__(self, age: int, gender: str, description: str):
        '''
        初始化 PersonalProfile 对象
        参数:
            age: 年龄 int
            gender: 性别 str
            description: 个人介绍 str
        '''
        self.age = age
        self.gender = gender
        self.description = description

class Student:
    '''学生模型'''
    def __init__(self, student_id: str, name: str, password: str, profile: PersonalProfile, dining_info_list: List[DiningInfo]):
        '''
        初始化 Student 对象
        参数:
            student_id: 学号 str
            name: 姓名 str
            password: 密码 str
            profile: 个人简介 PersonalProfile
            dining_info_list: 就餐信息列表 List[DiningInfo]
        '''
        self.student_id = student_id
        self.name = name
        self.password = password
        self.profile = profile
        self.dining_info_list = dining_info_list

    def validate(self):
        '''验证学生数据的有效性'''
        if not self.student_id:
            return None
        if not self.name:
            return None
        if not self.password:
            return None

    def __str__(self) -> str:
        '''返回学生的字符串表示'''
        return f"{self.name} ({self.student_id})"

    def __eq__(self, other) -> bool:
        '''比较两个学生对象是否相等'''
        if isinstance(other, Student):
            return self.student_id == other.student_id
        return False

def load_students_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    从 JSON 文件加载学生数据
    参数:
        file_path 文件路径(json文件) str
    返回：
        学生Json数据列表 List[Dict[str, Any]]
    """
    return load_json_list(file_path)

def convert_to_students(students_data: List[Dict[str, Any]]) -> List[Student]:
    '''
    转换 JSON 数据为学生对象
    参数:
        students_data 学生Json数据列表 List[Dict[str, Any]]
    返回:
        学生对象列表 List[Student]
    '''
    students = []
    for data in students_data:
        try:
            if not isinstance(data, dict):
                raise ValueError("每个学生数据应为字典")
            profile_data = data['profile']
            profile = PersonalProfile(
                age=profile_data['age'],
                gender=profile_data['gender'],
                description=profile_data['description']
            )
            dining_info_list = []
            for dining_data in data['dining_info_list']:
                dining_info = DiningInfo(
                    dining_time=datetime.fromisoformat(dining_data['dining_time']),
                    dishes=dining_data['dishes'],
                    remarks=dining_data['remarks'],
                    location=dining_data.get('location', "Unknown"),
                    images=dining_data.get('images', [])
                )
                dining_info_list.append(dining_info)
            student = Student(
                student_id=data['student_id'],
                name=data['name'],
                password=data['password'],
                profile=profile,
                dining_info_list=dining_info_list
            )
            students.append(student)
        except (KeyError, ValueError) as e:
            print(f"数据转换时出错: {e}")
    return students

def save_students_to_json(file_path: str, students: List[Student]) -> None:
    """
    将学生数据保存到 JSON 文件
    参数: 
        file_path 文件路径 str
        students 学生列表 List[Student]
    无返回
    """
    students_data = []
    for student in students:
        student_dict = student.__dict__.copy()
        student_dict['profile'] = student.profile.__dict__
        student_dict['dining_info_list'] = [
            {
                'dining_time': dining_info.dining_time.isoformat(),
                'dishes': dining_info.dishes,
                'remarks': dining_info.remarks,
                'location': dining_info.location,
                'images': dining_info.images if dining_info.images is not None else []
            } for dining_info in student.dining_info_list
        ]
        students_data.append(student_dict)
    save_json_list(file_path, students_data)
