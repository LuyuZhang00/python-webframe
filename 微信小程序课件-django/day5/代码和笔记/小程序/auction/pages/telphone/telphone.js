// pages/telphone/telphone.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    phone:"",
    code:""
  },
  bindPhone:function(e){
    this.setData({ phone:e.detail.value});
  },
  bindCode: function (e) {
    this.setData({ code: e.detail.value });
  },
  /**
   * 发送短信验证码
   */
  messageCode:function(){
    // 手机长度限制
    if (this.data.phone.length !=11){
      // 弹窗
      wx.showToast({
        title: '手机号长度错误',
        icon:"none", // loading/success/none
      })
      return;
    }

    // 正则匹配手机格式
    var reg = /^(1[3|4|5|6|7|8|9])\d{9}$/;
    if(!reg.test(this.data.phone)){
      wx.showToast({
        title: '手机号格式错误',
        icon: "none", // loading/success/none
      })
      return;
    }

    wx.request({
      url: 'http://127.0.0.1:8000/api/message/',
      data: { phone: this.data.phone },
      method: 'GET',
      success: function (res) {
        console.log(res);
      }
    })
  },
  /**
   * 用户登录
   */
  login:function(){
    console.log(this.data.phone, this.data.code);
      // 将手机号和验证码发送到后端，后端进行登录。
      wx.request({
        url: 'http://127.0.0.1:8000/api/login/',
        data: { phone: this.data.phone, code: this.data.code},
        method: 'POST',
        success: function(res) {
          console.log(res);
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