//app.js

App({
  onLaunch: function() {
    var userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    }
  },
  globalData: {
    userInfo: null
  },
  initUserInfo: function(tokenInfo, userInfo) {
    var info = {
      nickName: userInfo.nickName,
      avatarUrl: userInfo.avatarUrl,
      token: tokenInfo.token,
      phone: tokenInfo.phone
    };
    this.globalData.userInfo = info
    wx.setStorageSync('userInfo', info);
  },
  logoutUserInfo:function(){
    wx.removeStorageSync('userInfo');
    this.globalData.userInfo=null;
  }
})