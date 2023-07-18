// pages/chooseCoupon/chooseCoupon.js
var api = require('../../config/api.js')
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    auction:null,
    couponList:[],
  },
  radioChange:function(e){
    var index = e.detail.value;
    var coupon = null;
    if(index>=0){
      coupon = this.data.couponList[index];
    }
    var pages = getCurrentPages();
    var prevPage = pages[pages.length - 2];  //上一个页面
    prevPage.resetCoupon(coupon);
    
    wx.navigateBack();

  },
  getUserAuctionCoupon:function(){
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.ChooseCoupon,
      data:{
        auction:this.data.auction
      },
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          couponList:res.data
        })
      },
      fail: function (res) { },
      complete: function (res) { },
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      auction: options.auction
    })
    this.getUserAuctionCoupon();
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
    this.getUserAuctionCoupon();
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