from typing import List, Dict, Any
from Core.json_storage import load_json_list, save_json_list

class Dish:
    '''菜品模型'''
    def __init__(self, location: str, name: str, price: float, category: str, image_url: str, calories: float, \
                 allergens: List[str], description: str):
        '''
        初始化 Dish 对象
        参数:
            location: 菜品位置 str
            name: 菜品名称 str
            price: 菜品价格 float
            category: 菜品分类 str
            image_url: 菜品图片 URL str
            calories: 菜品热量 float
            allergens: 过敏源列表 List[str]
            description: 菜品描述 str
        '''
        self.location = location
        self.name = name
        self.price = price
        self.category = category
        self.image_url = image_url
        self.calories = calories
        self.allergens = allergens
        self.description = description
        # self.validate()

    '''Debug模式下显示菜品信息'''
    def display_info(self):
        return f"菜品名称: {self.name}\n价格: {self.price}元\n分类: {self.category}\n热量: {self.calories} \
    \n过敏源: {', '.join(self.allergens)}\n描述: {self.description} \
    位置:{self.location}"


    def __str__(self) -> str:
        '''返回菜品的字符串表示'''
        return f"{self.name} ({self.category}) - {self.price}元"

    def __eq__(self, other) -> bool:
        '''比较两个菜品对象是否相等'''
        if isinstance(other, Dish):
            return self.name == other.name and self.location == other.location
        return False

def load_dishes_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    从 JSON 文件加载菜品数据
    参数:
        file_path 文件路径(json文件) str
    返回：
        菜品Json数据列表 List[Dict[str, Any]]
    """
    return load_json_list(file_path)

def convert_to_dishes(dishes_data: List[Dict[str, Any]]) -> List[Dish]:
    '''
    转换 JSON 数据为菜品对象
    参数:
        dishes_data 菜品Json数据列表 List[Dict[str, Any]]
    返回:
        菜品对象列表 List[Dish]
    '''
    dishes = []
    for data in dishes_data:
        try:
            if not isinstance(data, dict):
                raise ValueError("每个菜品数据应为字典")
            dish = Dish(
                location=data.get("location", "Unknown"),
                name=data['name'],
                price=data['price'],
                category=data['category'],
                image_url=data['image_url'],
                calories=data['calories'],
                allergens=data['allergens'],
                description=data['description']
            )
            dishes.append(dish)
        except (KeyError, ValueError) as e:
            print(f"数据转换时出错: {e}")
    return dishes

def save_dishes_to_json(file_path: str, dishes: List[Dish]) -> None:
    """
    将菜品数据保存到 JSON 文件
    参数: 
        file_path 文件路径 str
        dishes 菜品列表 List[Dish]
    无返回
    """
    dishes_data = [dish.__dict__ for dish in dishes]  # 将菜品对象转换为字典
    save_json_list(file_path, dishes_data)
