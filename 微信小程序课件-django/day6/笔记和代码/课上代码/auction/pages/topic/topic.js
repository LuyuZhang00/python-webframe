// pages/topic/topic.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    topicList:[
      { id: 1, title:"春节买不到票",count:100},
      { id: 2, title: "黄牛太多", count: 100 },
      { id: 3, title: "票价太贵", count: 100 },
      { id: 4, title: "我有黄牛资源", count: 100 },
    ]
  },
  choseTopic:function(e){
    
    var topicInfo = e.currentTarget.dataset.xx;
    // 把这个值传递给他的父页面
    var pages = getCurrentPages();
    var prevPage = pages[pages.length-2];
    // prevPage.setData({ topicText:topicInfo.title });
    prevPage.setTopicData(topicInfo);

    wx.navigateBack({});
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // var that = this;
    // wx.request({
    //   url: '',
    //   data: '',
    //   header: {},
    //   method: 'GET',
    //   dataType: 'json',
    //   responseType: 'text',
    //   success: function(res) {
    //       that.setData({
    //         topicList: [
    //           { id: 1, title: "春节买不到票", count: 100 },
    //           { id: 2, title: "黄牛太多", count: 100 },
    //           { id: 3, title: "票价太贵", count: 100 },
    //           { id: 4, title: "我有黄牛资源", count: 100 },
    //         ]
    //       })
    //   },
    //   fail: function(res) {},
    //   complete: function(res) {},
    // })
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