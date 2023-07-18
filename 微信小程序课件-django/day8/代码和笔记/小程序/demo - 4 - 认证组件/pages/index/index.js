// pages/index/index.js

var api = require('../../config/api.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    newsList:[],
    maxId:0,
    minId:0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 去数据库获取最新的10条数据
    wx.request({
      url: api.NewsAPI,
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {        
        this.setData({
          newsList:res.data,
          maxId: res.data[0].id,
          minId: res.data[res.data.length - 1].id
        })
      },
      fail: function(res) {},
      complete: function(res) {},
    })
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
    wx.request({
      url: api.NewsAPI,
      data: {
        max_id:this.data.maxId
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        
        if(!res.data.length){
          wx.showToast({
            title: '已是最新数据',
            icon: 'none'
          })
          wx.stopPullDownRefresh()
          return
        }
        var dataList = res.data.reverse();
        this.setData({
          newsList: dataList.concat(this.data.newsList),
          maxId: dataList[0].id
        })
        wx.stopPullDownRefresh()
      }
    })
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    wx.request({
      url: api.NewsAPI,
      data: {
        min_id:this.data.minId
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
          if(!res.data.length){
            wx.showToast({
              title: '已到底部',
              icon: 'none'
            })
            return
          }
          this.setData({
            newsList: this.data.newsList.concat(res.data),
            minId: res.data[res.data.length-1].id
          })
      }
    })
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})