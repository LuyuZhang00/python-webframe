// pages/bid/bid.js
var api = require('../../config/api.js')
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    result: {},
    itemId: null
  },
  /**
   * 出价
   */
  doSubmit: function() {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Bid + "?item_id=" + this.data.itemId,
      data: {
        price: this.data.result.price,
        item: this.data.itemId
      },
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        if(res.statusCode == 201){
          this.setData({
            ['result.bid_list']:[res.data].concat(this.data.result.bid_list)
          })
        }
      },
    })
  },
  /**
   * 竞价
   */
  doCompete: function() {
    this.setData({
      'result.price': this.data.result.price + this.data.result.unit
    })
  },
  /**
   * 获取竞拍信息
   */
  getBidInfo: function() {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Bid,
      data: {
        item_id: this.data.itemId
      },
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          result: res.data
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.setData({
      itemId: options.itemId
    });
    this.getBidInfo();
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
    this.getBidInfo();
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