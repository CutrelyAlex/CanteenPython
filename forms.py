from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import DateTimeField, FileField, FloatField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import Length, DataRequired

class DishForm(FlaskForm):
    name = StringField(label="菜的名称", validators=[
        DataRequired(message="菜名不能为空"),
        Length(min=0, max=30,message="菜名不能超过30个字")
    ], render_kw={"class":"form-control", "placeholder":"请输入菜名"})

    category = StringField(label="菜的种类", validators=[
        DataRequired(message="种类不能为空"),
    ], render_kw={"class":"form-control", "placeholder":"请输入种类"})

    img_url = FileField(label="菜品图片",
    validators=[FileAllowed(upload_set=['png','jpg'],message="只能上传图片格式")],)
    
    calories = FloatField(label="热量",
            validators=[DataRequired(message="热量不能为空"),],
            render_kw={"class":"form-control", "placeholder":"请输入热量"})
    
    price = FloatField(label="菜的价格",
            validators=[DataRequired(message="价格不能为空"),],
            render_kw={"class":"form-control", "placeholder":"请输入价格"})

    location = SelectField(label="菜的位置",
    choices=[("北区","北区"),("南区","南区"),("南堕落街","南堕落街"),("西餐厅","西餐厅"),
    ("北堕落街","北堕落街"), ("竹韵食堂","竹韵食堂")], 
    render_kw={"class":"form-control custom-select", "placeholder":"请选择位置"})
    
    allergens = TextAreaField(label="菜的原材料", validators=[
        DataRequired(message="材料不能为空"),
    ], render_kw={"class":"form-control", "placeholder":"请输入材料", "rows":5, "cols":50})

    description = TextAreaField(label="菜品详情",
                validators=[DataRequired()],
                render_kw={"class":"form-control", "placeholder":"请输入菜的描述", "rows":5, "cols":50})


class StuForm(FlaskForm):
    student_id = StringField(label="学生学号",
    validators=[
        DataRequired(message="学号不能为空"),
        Length(min=12,max=12,message="学号必须为12位")
    ],
    render_kw={"class":"form-control", "placeholder":"请输入学号(12位)"})

    name = StringField(label="学生姓名",
    validators=[
        DataRequired(message="姓名不能为空"),
    ],
    render_kw={"class":"form-control", "placeholder":"请输入姓名"})

    password = StringField(label="学生密码",
    validators=[DataRequired(message="密码不能为空")],
    render_kw={"class":"form-control", "placeholder":"请输入密码"})

    age = IntegerField(label="学生年龄",
    validators=[DataRequired(message="学生年龄不能为空")],
    render_kw={"class":"form-control", "placeholder":"请输入年龄"})

    gender = SelectField(label="性别",
    choices=[("-1", "--请选择--") ,("男","男"),("女", "女")],
    render_kw={"class":"form-control"})

    description = TextAreaField(label="描述",
    validators=[DataRequired(message="材料不能为空")],
    render_kw={"class":"form-control", "rows":5, "cols":50})

    datetime = DateTimeField(label="就餐时间",
    format='%Y-%m-%d %H:%M:%S',
    default=datetime.now(),
    validators=[DataRequired(message="时间不能为空")],
    render_kw={"class":"form-control", "placeholder":"请输入就餐时间"})
    
    dishes = StringField(label="菜品（多个菜品用逗号隔开）",
    validators=[DataRequired(message="菜品不能为空")],
    render_kw={"class":"form-control", "placeholder":"请输入菜品"})

    remarks = TextAreaField(label="备注",
    render_kw={"class":"form-control", "rows":5, "cols":50})

    location = SelectField(label="位置",
    choices=[("北区","北区"),("南区","南区"),("南堕落街","南堕落街"),("西餐厅","西餐厅"),
    ("北堕落街","北堕落街"), ("竹韵食堂","竹韵食堂")], 
    render_kw={"class":"form-control"})
    
