// pages/coupon/coupon.js
var api = require("../../config/api.js")
var app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    couponList: []
  },
  applyCoupon: function(e) {
    if (e.currentTarget.dataset.item.status != 2) {
      return
    }
    var userInfo = app.globalData.userInfo;
    wx: wx.request({
      url: api.UserCoupon,
      data: {
        coupon: e.currentTarget.dataset.item.id
      },
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          ["couponList[" + e.currentTarget.dataset.index + "].remain"]: res.data.remain
        })
      },
      fail: function(res) {},
      complete: function(res) {},
    })
  },
  getCoupon: function() {
    wx: wx.request({
      url: api.Coupon,
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          couponList: res.data
        })
      },
      fail: function(res) {},
      complete: function(res) {},
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.getCoupon();
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {
    this.getCoupon();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})