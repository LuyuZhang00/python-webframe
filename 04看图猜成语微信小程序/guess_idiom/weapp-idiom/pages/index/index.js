//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    userInfo: {},
    hasUserInfo: false
  },
  onLoad: function () {
    if (app.globalData.userInfo == null) {
      this.bindLogin();
    }
  },
  onShow: function(){
    this.setData({
      userInfo: app.globalData.userInfo
    });
  },
  //开始游戏
  bindBegin: function () {
    var that = this;
    if (this.data.userInfo.level >= app.globalData.levelTotal) {
      wx.navigateTo({
        url: '../success/success'
      });
    } else {
      wx.navigateTo({
        url: '../guess/guess'
      });
    }
  },
  // 用户登录
  bindLogin: function (e) {
    var that = this;
    // 微信登录
    wx.login({
      success: function (loginRes) {
        if (loginRes.code) {
          // 查看是否授权
          wx.getSetting({
            success: function (res) {
              if (res.authSetting['scope.userInfo']) {
                // 微信获取用户信息
                wx.getUserInfo({
                  success: function (result) {
                    // 执行登录
                    that.wxlogin(loginRes.code,result.userInfo.nickName,result.userInfo.avatarUrl)
                  }
                });
              } else {
                wx.showToast({
                  title: '请先授权用户信息',
                  icon: "none"
                });
              }
            }
          });
        }
      }
    });
  },
  // 服务器登录
  wxlogin: function (code,nickname,avatar) {
    var that = this;
    wx.showLoading({
      title: '正在登录中',
      mask: true
    });
    wx.request({
      url: app.globalData.URL + '/api/users/wx_login',
      data: {
        code: code,
        nickname:nickname,
        avatar:avatar,
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        console.log(res)
        var data = res.data.result.data
        // 将token写入缓存
        try {
          wx.setStorageSync('token', data.token)
        } catch (e) {
          console.log('storage token error')
        }
        app.globalData.levelTotal = data.total_level;
        app.globalData.userInfo = data.user_info;
        that.setData({
            userInfo: data.user_info,
            hasUserInfo: true
        });
      },
      fail: function () {
        console.log("wxlogin fail");
        wx.showToast({
          title: '登录失败',
          icon: 'none'
        });
      },
      complete: function () {
        wx.hideLoading();
      }
    });
  },
  // 查看排行榜
  bindRank: function(){
    wx.navigateTo({
      url: '../rank/rank'
    });
  }
})
