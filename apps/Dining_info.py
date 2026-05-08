from flask import Blueprint, render_template

from Core.StudentController import StudentController

dining_bp = Blueprint('dining', __name__ ,url_prefix='/dining')

'''就餐记录'''
@dining_bp.route('/dining_list', methods=['GET','POST'])
def dining_list():
    get_stus = StudentController().get_all_students()
    return render_template('MangerStu/Dining_record.html', get_stus=get_stus)
