// component/tabbar/tabbar.js
var app = getApp()
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    selected:{
      type:Number,
      value:0
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    color: "#7A7E83",
    selectedColor: "#DC143C",
    list: [{
      pagePath: "/pages/index/index",
      iconPath: "/static/tabbar/ic_menu_choice_nor.png",
      selectedIconPath: "/static/tabbar/ic_menu_choice_pressed.png",
      text: "首页"
    }, {
      text: "发布"
    }, 
    {
      pagePath: "/pages/home/home",
        iconPath: "/static/tabbar/ic_menu_me_nor.png",
        selectedIconPath: "/static/tabbar/ic_menu_me_pressed.png",
      text: "我的"
    }]
  },

  /**
   * 组件的方法列表
   */
  methods: {
    
    switchTab(e) {
      var data = e.currentTarget.dataset
      var url = data.path;
      if(url){
        wx.switchTab({ url });
      }else{
        if(app.globalData.userInfo){
          wx.navigateTo({
            url: '/pages/publish/publish',
          })
        }else{
          wx.navigateTo({
            url: '/pages/auth/auth',
          })
        }


      }

      
    }
  }
})
