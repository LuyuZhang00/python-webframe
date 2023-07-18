// pages/rank/rank.js
//获取应用实例
const app = getApp();

Page({
  /**
   * 页面的初始数据
   */
  data: {
    rankData: [],
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.bindRank();
  },
  bindRank: function () {
    var that = this;
    wx.showLoading({
      title: '数据加载中',
      mask: true
    });
    wx.request({
      url: app.globalData.URL + '/api/games/rank',
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": "Bearer " + wx.getStorageSync('token'),
      },
      success: function (res) {
        if (res.data.result.code == 1) {
          that.setData({
            rankData: res.data.result.data
          });
        } else {
          wx.showToast({
            title: res.data.result.msg,
            mask: true
          });
        }
      },
      fail: function () {
        console.log("post index/rank fail");
      },
      complete: function () {
        wx.hideLoading();
      }
    });
  }
})
