// pages/auctionDetail/auctionDetail.js
var api = require('../../config/api.js')
var auth = require('../../utils/auth.js')
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    auctionDetail: {},
    auctionId: null
  },

  getDetailInfo:function(){
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Auction + this.data.auctionId + '/',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          auctionDetail: res.data
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.setData({
      auctionId: options.auctionId
    });
    
    this.getDetailInfo();
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
    this.getDetailInfo();
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

  },

  /*
   * 缴纳保证金
   */
  payDeposit: function(e) {
    var itemId = e.currentTarget.dataset.itemid;
    if (auth.authentication) {
      wx.navigateTo({
        url: '/pages/deposit/deposit?itemId=' + itemId
      })
    }
  },
  /**
   * 去竞拍
   */
  toBid: function(e) {
    var itemId = e.currentTarget.dataset.itemid;
    if (auth.authentication) {
      wx.navigateTo({
        url: '/pages/bid/bid?itemId=' + itemId
      })
    }

  }
})