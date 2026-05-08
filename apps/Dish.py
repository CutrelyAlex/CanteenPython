import os

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from Core.DishController import DishController
from forms import DishForm
'''
    建立菜品蓝图
    有以下几个主要函数：
        dish_list() 显示菜品列表页面
        dish_add() 添加菜品页面
        dish_edit() 修改菜品页面
        diish_delete 删除菜品页面
'''

dish_bp = Blueprint("dish", __name__, url_prefix='/dish') # 建立菜品蓝图 url: /dish/
dishInit = DishController() # 初始化菜品对象
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "img")


def _parse_legacy_dish_id(dish_id: str):
    """Parse legacy dish id format: ('name', 'location')."""
    if not dish_id:
        return None
    if not (dish_id.startswith("(") and dish_id.endswith(")")):
        return None
    inner = dish_id[1:-1]
    parts = inner.split(",", 1)
    if len(parts) != 2:
        return None
    dish_name = parts[0].strip().strip("'\"")
    dish_location = parts[1].strip().strip("'\"")
    if not dish_name or not dish_location:
        return None
    return dish_name, dish_location

'''菜品列表'''
@dish_bp.route('/dish_list', methods=['GET','POST'])
def dish_list():
    if request.method == 'GET':
        dishes = dishInit.get_all_dishes()
        return render_template("MangerDish/index.html", dishes=dishes, dishInit=dishInit)
    if request.method == 'POST':
        name = request.form.get("name")
        location = request.form.get("location")
        if name and location != '-1': # -1表示未选择
            dishes = dishInit.find_dish_by_location(location, name)
        elif name and location == '-1':
            dishes = dishInit.find_dish_by_name(name)
        elif not name and location != '-1':
            dishes = dishInit.get_all_dishes_by_location(location)
        else:
            dishes = dishInit.get_all_dishes()
        return render_template("MangerDish/index.html",
                dishes=dishes)

'''添加菜品'''
@dish_bp.route('/dish_add', methods=['GET','POST'])
def dish_add():
    f = DishForm()
    if f.validate_on_submit():
        img = request.files['img_url']
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image_filename = secure_filename(img.filename) if img.filename else ""
        if image_filename:
            img.save(os.path.join(UPLOAD_FOLDER, image_filename))
        exist_location = []
        names = dishInit.find_dish_by_name(f.name.data) # 查找餐品名
        for name in names:
            exist_location.append(name.location)
        if names and f.location.data in exist_location:
            flash("菜品已存在，请查询")
            return render_template("MangerDish/add.html", form=f)
        else:
            toListAllergens = f.allergens.data.split() # 将str:allergens --> list:allergens
            dishInit.add_dish(location=f.location.data, name=f.name.data,
            price=f.price.data, category=f.category.data, image_url=image_filename, allergens=toListAllergens,
            description=f.description.data, calories=f.calories.data)
            return redirect('dish_list')
    return render_template('MangerDish/add.html', form=f)

'''修改菜品'''
@dish_bp.route('/dish_edit', methods=['GET', 'POST'])
@dish_bp.route('/dish_edit/<dish_id>', methods=['GET', 'POST'])
def dish_edit(dish_id=None):
    if request.method == 'GET':
        dish_name = request.args.get("name", "").strip()
        dish_location = request.args.get("location", "").strip()
        if (not dish_name or not dish_location) and dish_id:
            legacy_dish = _parse_legacy_dish_id(dish_id)
            if legacy_dish:
                dish_name, dish_location = legacy_dish
    else:
        dish_name = request.form.get("dish_name", "").strip()
        dish_location = request.form.get("dish_location", "").strip()

    if not dish_name or not dish_location:
        flash("菜品参数错误")
        return redirect(url_for("dish.dish_list"))

    matched_dishes = dishInit.find_dish_by_location(dish_location, dish_name)
    if not matched_dishes:
        flash("未找到菜品")
        return redirect(url_for("dish.dish_list"))
    dish_obj = matched_dishes[0] # 根据菜名获得菜品全部信息
    if request.method == 'GET':
        # print(dish_obj)
        f = DishForm()
        str_allergen = "" # 将allergens列表形式转换成字符串输出
        for allergen in dish_obj.allergens:
            str_allergen += " " + allergen
        str_allergen = str_allergen.strip()
        # f.name.data = dish_obj.name
        f.category.data = dish_obj.category
        f.img_url.data = dish_obj.image_url
        f.calories.data = dish_obj.calories
        f.price.data = dish_obj.price
        # f.location.data = dish_obj.location
        f.allergens.data = str_allergen
        f.description.data = dish_obj.description
        return render_template('MangerDish/edit.html', form=f, dish_name=dish_name, dish_location=dish_location)
    elif request.method == 'POST':
        f = DishForm(request.form)
        if f.is_submitted(): # 检测是否获取了表单,不能通过validate验证？？？
            # toListAllergens = f.allergens.data.split()
            img = request.files['img_url']
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            image_filename = secure_filename(img.filename) if img.filename else ""
            if image_filename:
                img.save(os.path.join(UPLOAD_FOLDER, image_filename))
            toListAllergens = f.allergens.data.split()
            update_kwargs = {
                "location": dish_location,
                "name": dish_name,
                "price": f.price.data,
                "category": f.category.data,
                "calories": f.calories.data,
                "allergens": toListAllergens,
                "description": f.description.data,
            }
            if image_filename:
                update_kwargs["image_url"] = image_filename
            dishInit.update_dish(**update_kwargs)
            return redirect(url_for('dish.dish_list'))
        else:
            return render_template('MangerDish/edit.html', form=f, dish_name=dish_name, dish_location=dish_location)

'''删除菜品'''
@dish_bp.route('/dish_del', methods=['GET', 'POST'])
def dish_del():
    dish_name = request.values.get("name", "").strip()
    dish_location = request.values.get("location", "").strip()
    if not dish_name or not dish_location:
        return jsonify({"code": 400, "message": "参数错误"}), 400
    dishInit.remove_dish(dish_name, dish_location)
    return jsonify({'code': 200})
