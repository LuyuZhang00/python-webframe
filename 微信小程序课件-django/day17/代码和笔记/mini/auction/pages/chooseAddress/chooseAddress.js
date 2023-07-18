// pages/chooseAddress/chooseAddress.js
var api = require("../../config/api.js")
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    addressList: [],
    address: {
      name: "",
      phone: "",
      detail: ""
    }
  },
  radioChange:function(e){
    var pages = getCurrentPages();
    var prevPage = pages[pages.length - 2];  //上一个页面
    
    var index = e.detail.value;
    var address = this.data.addressList[index];
    prevPage.setData({
      address: address
    })
    wx.navigateBack();
  },
  inputUser: function(e) {
    this.setData({
      ["address.name"]: e.detail.value
    })
  },
  inputPhone: function(e) {
    this.setData({
      ["address.phone"]: e.detail.value
    })
  },
  inputDetail: function(e) {
    this.setData({
      ["address.detail"]: e.detail.value
    })
  },

  addAddress: function() {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Address,
      data: this.data.address,
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        console.log(res);
        if (res.statusCode == 201) {
          var newList = this.data.addressList;
          newList.push(res.data)
          this.setData({
            addressList: newList
          })
        } else {
          wx: wx.showToast({
            title: '添加失败',
            icon: 'none'
          })
        }
        
      },
      fail: function(res) {},
      complete: function(res) {},
    })
  },
  getAddressList: function() {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Address,
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          addressList: res.data
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
    this.getAddressList();
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
    this.getAddressList();
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