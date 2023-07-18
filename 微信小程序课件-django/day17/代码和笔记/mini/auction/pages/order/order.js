// pages/order/order.js
var api = require('../../config/api.js')
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    seleted:null,
    orderDict:{}
  },
  toPay:function(e){
    var order = e.currentTarget.dataset.item;
    if(order.status != 1){
      return
    }
    wx.navigateTo({url: '/pages/pay/pay?orderId=' + order.id});

  },
  changeStatus: function (e) {
    var seleted = e.currentTarget.dataset.id;
    this.setData({
      seleted: seleted
    })
  },
  getOrder:function(){
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Order,
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          orderDict: res.data
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
      seleted:options.seleted
    })
    this.getOrder();
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
    this.getOrder();
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