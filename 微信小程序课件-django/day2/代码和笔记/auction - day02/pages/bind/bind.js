// pages/bind/bind.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    message:"沙雕李业",
    name:"",
    path:"/static/default.png"
  },
  changeData:function(){

    // 获取数据
    console.log(this.data.message);

    // 修改数据(错误，只改后端)
    // this.data.message = "大沙雕李业";

    // 修改数据
    this.setData({ message: "大沙雕李业"});

  },

  xxxx:function(){
    var that = this;
    //this.setData()
    // 调用微信的接口，获取当前用户信息
    wx.getUserInfo({
      success: function (res) {
        // 调用成功后触发
        console.log('success',res)
        that.setData({ 
          name: res.userInfo.nickName,
          path: res.userInfo.avatarUrl
          });
      },
      fail:function(res){
        // 调用失败后触发
        console.log('fail', res)
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