// pages/home/home.js

var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: null
  },

  /**
   * 生命周期函数--监听页面加载(第一次打开时会执行)
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成（第一次打开时会执行）
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    //本地storage中获取值
    this.setData({
      userInfo: app.globalData.userInfo
    })
  },
   /**
   * 用户注销
   */
  onClickLogout:function(){
    app.delUserInfo();
    this.setData({
      userInfo: null
    })
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

  }
})