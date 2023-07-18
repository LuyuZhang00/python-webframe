from fastapi import APIRouter
from models import *
from pydantic import BaseModel, validator
from typing import List, Union
from fastapi.templating import Jinja2Templates
from fastapi import Request

from fastapi.exceptions import HTTPException

student_api = APIRouter()


@student_api.get("/")
async def getAllStudent():
    # (1) 查询所有 all方法
    students = await Student.all()  # Queryset: [Student(),Student(),Student()]
    # print("students", students)
    #
    # for stu in students:
    #     print(stu.name, stu.sno)
    # print(students[0].name)
    # (2) 过滤查询 filter
    # students = await Student.filter(name="rain")  # Queryset: [Student(),Student(),Student()]
    # students = await Student.filter(clas_id=14)  # Queryset: [Student(),Student(),Student()]
    # print("students", students)

    # (3) 过滤查询 get方法：返回模型类型对象

    # stu = await Student.filter(id=6)  # [Student(),]
    # print(stu[0].name)
    # stu = await Student.get(id=6)  # Student()
    # print(stu.name)

    # (4) 模糊查询
    # stus = await Student.filter(sno__gt=2001)
    # stus = await Student.filter(sno__range=[1, 10000])
    # stus = await Student.filter(sno__in=[2001, 2002])
    # print(stus)  # [<Student: 7>, <Student: 8>]

    # (5) values查询
    # stus = await Student.filter(sno__range=[1, 10000])  # [Student(),Student(),Student(),...]
    # stus = await Student.all().values("name", "sno")  # [{},{},{},...]
    # print(stus)

    # (6) 一对多查询 多对多查询
    alvin = await Student.get(name="alvin")
    print(alvin.name)
    print(alvin.sno)
    print(await alvin.clas.values("name"))  # {'name': '计算机科学与技术2班'}
    students = await Student.all().values("name", "clas__name")
    print(await alvin.courses.all().values("name", "teacher__name"))
    students = await Student.all().values("name", "clas__name", "courses__name")

    return students


@student_api.get("/index.html")
async def getAllStudent(request: Request):
    templates = Jinja2Templates(directory="templates")
    students = await Student.all()  # [Student(),Student(),...]

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "students": students
        }
    )


class StudentIn(BaseModel):
    name: str
    pwd: str
    sno: int
    clas_id: int
    courses: List[int] = []

    @validator("name")
    def name_must_alpha(cls, value):
        assert value.isalpha(), 'name must be alpha'
        return value

    @validator("sno")
    def sno_validate(cls, value):
        assert 1000 < value < 10000, '学号要在2000-10000的范围内'
        return value


@student_api.post("/")
async def addStudent(student_in: StudentIn):
    # 插入到数据库
    # 方式1
    # student = Student(name=student_in.name, pwd=student_in.pwd, sno=student_in.sno, clas_id=student_in.clas_id)
    # await student.save() # 插入到数据库student表
    # 方式2
    student = await Student.create(name=student_in.name, pwd=student_in.pwd, sno=student_in.sno,
                                   clas_id=student_in.clas_id)

    # 多对多的关系绑定
    choose_courses = await Course.filter(id__in=student_in.courses)
    await student.courses.add(*choose_courses)

    return student


@student_api.get("/{student_id}")
async def getOneStudent(student_id: int):
    student = await Student.get(id=student_id)

    return student


@student_api.put("/{student_id}")
async def updateStudent(student_id: int, student_in: StudentIn):
    data = student_in.dict()
    print("data", data)
    courses = data.pop("courses")

    await Student.filter(id=student_id).update(**data)

    #  设置多对多的选修课
    edit_stu = await Student.get(id=student_id)
    choose_courses = await Course.filter(id__in=courses)
    await edit_stu.courses.clear()
    await edit_stu.courses.add(*choose_courses)

    return edit_stu


@student_api.delete("/{student_id}")
async def deleteStudent(student_id: int):
    deleteCount = await Student.filter(id=student_id).delete()
    if not deleteCount:
        raise HTTPException(status_code=404, detail=f"主键为{student_id}的学生不存在")

    return {}
