// pages/login/login.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    phone:null
  },
  inputPhone:function(e){
    this.setData({
      phone:e.detail.value
    })
  },  

  doSubmit:function(e){
    wx.login({
      success:(result) => {
        // 获取一个临时凭证（只能用一次/5分钟）
        wx.request({
          url: 'http://127.0.0.1:8002/login/',
          data: {
            phone:this.data.phone,
            wx_code:result.code
          },
          method: 'POST',
          dataType: 'json',
          responseType: 'text',
          success: (res) => {
            console.log('登录成功');
          }
        })
      }
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