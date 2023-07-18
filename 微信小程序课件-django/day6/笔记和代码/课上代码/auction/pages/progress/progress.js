// pages/progress/progress.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    percent1:20,
    percent2:50,
    imageList:[
      {id:1,title:"图片1",percent:20},
      { id: 1, title: "图片2", percent: 30 },
      { id: 1, title: "图片3", percent: 60 },
    ]
  },
  changePercent:function(){
    // 方式2：可以，由于需要全部修改，所以性能差。
    /*
    var dataList = this.data.imageList;
    dataList[0].percent = 80;
    this.setData({
      imageList: dataList
    });
    */

    // 方式3：推荐
    var num = 2;
    this.setData({
      ["imageList[0].percent"]:80,
      ["imageList[" + num + "].percent"]: 90,
      ["imageList[1].title"]:"突突突突突"
    })

  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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