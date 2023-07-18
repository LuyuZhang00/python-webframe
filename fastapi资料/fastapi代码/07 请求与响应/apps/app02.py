from fastapi import APIRouter
from typing import Union, Optional

app02 = APIRouter()


@app02.get("/jobs/{kd}")
async def get_jobs(kd: str, xl: Union[str, None] = None, gj: Optional[str] = None):  # 没有默认参数即前端必须输入
    # 基于kd, xl, gj数据库查询岗位信息
    return {
        "kd": kd,
        "xl": xl,
        "gj": gj,
    }
