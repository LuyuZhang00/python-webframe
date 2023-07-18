// components/tabbar/tabbar.js
var auth = require('../../utils/auth.js')
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    selected: {
      type: Number,
      value: 0
    }
  },
  /**
   * 组件的初始数据
   */
  data: {
    color: "#7A7E83",
    selectedColor: "#b4282d",
    list: [{
        "pagePath": "/pages/index/index",
        "text": "首页",
        "iconPath": "/static/images/tabbar/ic_menu_choice_nor.png",
        "selectedIconPath": "/static/images/tabbar/ic_menu_choice_pressed.png"
      },
      {
        "pagePath": "/pages/auction/auction",
        "text": "拍卖",
        "iconPath": "/static/images/tabbar/ic_menu_topic_nor.png",
        "selectedIconPath": "/static/images/tabbar/ic_menu_topic_pressed.png"
      },
      {
        "text": "发布"
      },
      {
        "pagePath": "/pages/message/message",
        "text": "消息",
        "iconPath": "/static/images/tabbar/ic_menu_shopping_nor.png",
        "selectedIconPath": "/static/images/tabbar/ic_menu_shopping_pressed.png"
      },
      {
        "pagePath": "/pages/home/home",
        "text": "我的",
        "iconPath": "/static/images/tabbar/ic_menu_me_nor.png",
        "selectedIconPath": "/static/images/tabbar/ic_menu_me_pressed.png"
      }
    ]
  },

  /**
   * 组件的方法列表
   */
  methods: {
    switchTab(e) {
      const data = e.currentTarget.dataset;
      const url = data.path;
      if (data.path) {
        wx.switchTab({
          url
        })
        return
      }
      var result = auth.authentication();
      if (result) {
        wx.navigateTo({
          url: '/pages/publish/publish',
        })
      }
    }
  }
})