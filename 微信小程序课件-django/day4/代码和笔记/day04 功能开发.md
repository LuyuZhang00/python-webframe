# day04 功能开发

## 内容回顾

- 组件
  - view
  - text
  - image
  - button
  - navigtor
  - textarea
  - input
- api
  - 用户信息
  - 地理位置
  - 选择图片
  - 跳转（非tabbar）
  - 打开授权配置
  - 发送请求（https/后台设置）
  - 提示框
- 数据绑定
  - setData
- 腾讯云发送短信服务
  - 后台配置频率
  - 调用API进行发送：v3版本



## 今日概要

- 用户登录/注册
- 发布心情
  - 图片上传（腾讯对象存储）
- 查看心情
- 查看心情详细



## 今日详细

### 1. 用户登录

### 1.1 发送短信

### 1.2 登录

- 小程序公共对象

  - app.js

    ```js
    App({
    
      /**
       * 当小程序初始化完成时，会触发 onLaunch（全局只触发一次）
       */
      onLaunch: function () {
    
      },
      globalData:{
        userInfo: null, 
      }
    })
    ```

  - 其他页面操作公共值

    ```
    var app = getApp();
    Page({
    	data: {
      	},
      	onShow:function(){
      		app.globalData
      	}
    });
    ```

    注意：修改globalData之后，其他页面以用的值不会自动变化，而是需要手动设置。

- 本地存储操作

  ```
  wx.getStorageSync('userInfo');
  wx.setStorageSync('userInfo',"sdfsfd");
  wx.removeStorageSync("userInfo")
  ```

- 页面调用栈

  ```
  var pages = getCurrentPages();
  prevPage = pages[pages.length-2];
  ```

- 跳转回上一个页面

  ```
  wx.navigateBack({});
  ```

- 小程序页面的生命周期

  - onLoad（一次）
  - onShow（只要展示这个页面，就会自动加载）
  - onReady（一次）
  - onHide（每次页面隐藏就会自动加载，）
  - onUnload（卸载页面，小程序关闭）

- 全局app.js

  ```
  App({
  
    /**
     * 当小程序初始化完成时，会触发 onLaunch（全局只触发一次）
     */
    onLaunch: function () {
  
    },
    globalData:{
      userInfo: null, 
    }
  })
  ```

- wx:if指令



## 作业

- 登录逻辑

- 对象存储上传文件：官方文档有代码。

- 表结构的设计（业务逻辑设计表结构）

  

















