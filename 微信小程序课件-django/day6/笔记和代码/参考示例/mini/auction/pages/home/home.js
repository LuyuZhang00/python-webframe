// pages/home/home.js

var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo:null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo
      });
    }else{
      this.setData({
        userInfo: null
      });
    }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  onClickLogin:function(){
    
    // var openid = wx.getStorageSync('openid');
    // console.log(openid);
    wx.login({
      success:function(res) {
        wx.request({
          url: 'http://127.0.0.1:8000/api/login/',
          method: "post",
          data:{ code:res.code},
          success:function(response){
            console.log(response.data);
            // jwt 认证
            wx.setStorageSync('session_key', response.data.session_key);
            wx.setStorageSync('openid', response.data.openid);
            wx.setStorageSync('code', res.code);
          }
        })
      },
      fail:function(res){

      },
      complete:function(){

      }
    })

  },
  getUserInfoFunction:function(e){
    console.log(e.detail);
  },
  onClickCall:function(){
    wx.makePhoneCall({
      phoneNumber: '15131255089'
    })
  },
  logout:function(){
    app.logoutUserInfo();
    
    this.setData({userInfo:null});
  }
})