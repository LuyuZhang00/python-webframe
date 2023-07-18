// pages/deposit/deposit.js
var api = require('../../config/api.js')
var app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    info: {},
    seletedPayMethod: 1
  },
  /*
   * 立即支付
   */
  onClickPayNow: function() {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.PayDeposit,
      data: {
        auction_id: this.data.info.auction_id,
        item_id: this.data.info.id,
        deposit_type: this.data.info.deposit.selected,
        amount: this.data.info.deposit.money,
        pay_type: this.data.seletedPayMethod
      },
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'post',
      success: res => {
        wx.requestPayment({
          timeStamp: res.data.timeStamp,
          nonceStr: res.data.nonceStr,
          package: res.data.package,
          signType: res.data.signType,
          paySign: res.data.paySign,
          success: (pay) => {
            // 如果是全场保证金，则设置 total=true
            // 如果是单品保证金，则设置 single = {itemID:true}
            var pages = getCurrentPages();
            var prevPage = pages[pages.length - 2]; //上一个页面
            if (this.data.info.deposit.selected == 1){
              // 如果是单品保证金，则设置 single = {itemID:true}
              prevPage.setData({
                ["auctionDetail.deposit.total.single[" + this.data.info.id +"]"]: true
              })
            }else{
              // 如果是全场保证金，则设置 total = true
              prevPage.setData({
                ["auctionDetail.deposit.total"]:true
              })
            }
            
            wx.navigateBack({});

          },
          fail: function(pay) {
            wx.showToast({
              title: '支付失败',
              icon: 'none'
            });
            console.log(pay);
          },
          complete: function(pay) {
            console.log('完成', pay);
          }
        })
      }
    });
  },
  /**
   * 支付方式
   */
  payMehthodChange: function(e) {
    this.setData({
      seletedPayMethod: e.detail.value
    });
  },
  /**
   * 单品or全场保证金
   */
  depositChange: function(e) {
    var row = this.data.info.deposit.list[e.detail.value];
    this.setData({
      ['info.deposit.selected']: row.id,
      ['info.deposit.money']: row.money,
    });
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.AuctionDeposit + options.itemId + '/',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          info: res.data,
          deposit_list: res.data.deposit_list
        });
      }
    })

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


})