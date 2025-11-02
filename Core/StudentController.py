"""
StudentController 模块

提供以下接口:
- add_student(location: str, name: str, student_id: str, password: str, profile: str, dining_info_list: List[DiningInfo]): 添加学生
- find_student_by_id(student_id: str) -> Student: 根据学号查找学生
- find_student_by_name(name: str) -> List[Student]: 根据姓名查找学生
- get_all_students() -> List[Student]: 获取所有学生
- remove_student(student_id: str): 根据学号删除学生
- update_student(student_id: str, **kwargs): 更新学生信息
- add_dining_record(student_id: str, dining_info: DiningInfo): 添加餐饮记录
- remove_dining_record(student_id: str, record_id: str): 删除餐饮记录
- find_dining_record(student_id: str, record_id: str) -> DiningInfo: 查找餐饮记录
- update_dining_record(student_id: str, record_id: str, **kwargs): 更新餐饮记录
"""

import re
from typing import List
from Core.StudentModel import Student, convert_to_students, load_students_from_json, save_students_to_json, DiningInfo
from Core.DishModel import Dish
from Core.StudentModel import PersonalProfile

student_path = "students.json"

class StudentController:
    """
    管理学生的控制器类。

    方法可能返回 `None`，例如在添加已存在的学生或未找到特定学生时。
    """
    def __init__(self):
        self.students = convert_to_students(load_students_from_json(student_path))
    
    def add_student(self, name: str, student_id: str, password: str, profile: dict, dining_info_list: List[DiningInfo]):
        """
        添加学生。

        参数:
            name (str): 学生的姓名
            student_id (str): 学生的学号
            password (str): 学生的密码
            profile (dict): 学生的简介，包含以下键值对:
                - age (int): 年龄
                - gender (str): 性别
                - description (str): 个人介绍
            dining_info_list (List[DiningInfo]): 学生的餐饮记录列表

        返回:
            None 如果学生已存在
        """
        for existing_student in self.students:
            if existing_student.student_id == student_id:
                return None
        new_profile = PersonalProfile(**profile)
        new_student = Student(student_id, name, password, new_profile, dining_info_list)
        self.students.append(new_student)
        save_students_to_json(student_path, self.students)
    
    def find_student_by_id(self, student_id: str) -> Student:
        """
        根据学号查找学生。

        参数:
            student_id (str): 学生的学号

        返回:
            Student: 找到的学生对象
            None 如果未找到
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def find_student_by_name(self, name: str) -> List[Student]:
        """
        根据姓名查找学生。

        参数:
            name (str): 学生的姓名

        返回:
            List[Student]: 匹配的学生列表
        """
        pattern = re.compile(name, re.IGNORECASE)
        matched_students = [student for student in self.students if pattern.search(student.name)]
        return matched_students
    
    def get_all_students(self) -> List[Student]:
        """
        获取所有学生。

        返回:
            List[Student]: 所有学生列表
        """
        return self.students
    
    def remove_student(self, student_id: str):
        """
        根据学号删除学生。

        参数:
            student_id (str): 要删除学生的学号

        返回:
            None
        """
        self.students = [student for student in self.students if student.student_id != student_id]
        save_students_to_json(student_path, self.students)
    
    def update_student(self, student_id: str, **kwargs):
        """
        更新学生信息。

        参数:
            student_id (str): 学生的学号
            **kwargs: 需要更新的字段及其新值，包括:
                - name (str): 姓名
                - password (str): 密码
                - profile (dict): 个人简介，包含以下键值对:
                    - age (int): 年龄
                    - gender (str): 性别
                    - description (str): 个人介绍
                - dining_info_list (List[DiningInfo]): 餐饮记录列表

        返回:
            None 如果学生未找到
        """
        for student in self.students:
            if student.student_id == student_id:
                if 'name' in kwargs:
                    student.name = kwargs['name']
                if 'password' in kwargs:
                    student.password = kwargs['password']
                if 'profile' in kwargs:
                    profile_data = kwargs['profile']
                    if isinstance(student.profile, dict):
                        student.profile = PersonalProfile(**profile_data)
                    student.profile.age = profile_data.get('age', student.profile.age)
                    student.profile.gender = profile_data.get('gender', student.profile.gender)
                    student.profile.description = profile_data.get('description', student.profile.description)
                if 'dining_info_list' in kwargs:
                    student.dining_info_list = kwargs['dining_info_list']
                save_students_to_json(student_path, self.students)
                return
        return None

    def add_dining_record(self, student_id: str, dining_info: DiningInfo):
        """
        添加餐饮记录。

        参数:
            student_id (str): 学生的学号
            dining_info (DiningInfo): 要添加的餐饮记录对象

        返回:
            None 如果学生未找到
        """
        for student in self.students:
            if student.student_id == student_id:
                student.dining_info_list.append(dining_info)
                save_students_to_json(student_path, self.students)
                return
        return None

    def remove_dining_record(self, student_id: str, record_id: str):
        """
        删除餐饮记录。

        参数:
            student_id (str): 学生的学号
            record_id (str): 餐饮记录的ID

        返回:
            None 如果记录未找到
        """
        for student in self.students:
            if student.student_id == student_id:
                original_length = len(student.dining_info_list)
                student.dining_info_list = [
                    record for record in student.dining_info_list if record.id != record_id
                ]
                if len(student.dining_info_list) < original_length:
                    save_students_to_json(student_path, self.students)
                    return
                else:
                    return None
        return None

    def find_dining_record(self, student_id: str, record_id: str) -> DiningInfo:
        """
        查找餐饮记录。

        参数:
            student_id (str): 学生的学号
            record_id (str): 餐饮记录的ID

        返回:
            DiningInfo: 找到的餐饮记录对象
            None 如果未找到
        """
        for student in self.students:
            if student.student_id == student_id:
                for record in student.dining_info_list:
                    if record.id == record_id:
                        return record
        return None

    def update_dining_record(self, student_id: str, record_id: str, **kwargs):
        """
        更新餐饮记录。

        参数:
            student_id (str): 学生的学号
            record_id (str): 餐饮记录的ID
            **kwargs: 需要更新的字段及其新值

        返回:
            None 如果记录未找到
        """
        for student in self.students:
            if student.student_id == student_id:
                for record in student.dining_info_list:
                    if record.id == record_id:
                        if 'dining_time' in kwargs:
                            record.dining_time = kwargs['dining_time']
                        if 'dishes' in kwargs:
                            record.dishes = kwargs['dishes']
                        if 'remarks' in kwargs:
                            record.remarks = kwargs['remarks']
                        if 'location' in kwargs:
                            record.location = kwargs['location']
                        if 'images' in kwargs:
                            record.images = kwargs['images'] 
                        save_students_to_json(student_path, self.students)
                        return
        return None