// pages/pay/pay.js
var api = require('../../config/api.js')
var app = getApp();

Page({
  /**
   * 页面的初始数据
   */
  data: {
    orderId: null,
    order: {},
    payPrice: null,
    address:null
  },
  doClickPay: function() {
    var info = {
      order_id: this.data.orderId,
      coupon_id: this.data.order.coupon.id,
      use_deposit: this.data.order.deposit.checked,
      address_id: this.data.address ? this.data.address.id : null,
      pay_type: this.data.order.pay_method.selected,
      real_pay: this.data.payPrice
    }
    // 将数据提交到后，支付成功，则跳转到成功页面；支付失败，提示错误信息
    console.log(info);
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.PayNow,
      data: info,
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        if (ret.statusCode == 200){
          wx.navigateTo({ url: '/pages/paySuccess/paySuccess' })
        }else{
          console.log('详细错误信息',res.data)
          wx.showToast({
            title: '订单支付失败',
            icon: 'none'
          })
        }
      },
      fail: function (res) { },
      complete: function (res) { },
    })
  },
  radioChange:function(e){
    this.setData({
      ["order.pay_method.selected"]: e.detail.value
    })
  },
  resetCoupon: function(coupon) {
    if (!coupon) {
      // 没有选择优惠券
      this.setData({
        ["order.coupon.id"]: null,
        ["order.coupon.text"]: "无",
        ["order.coupon.money"]: 0
      })
    }else{
      // 选择了优惠券
      this.setData({
        ["order.coupon.id"]: coupon.id,
        ["order.coupon.text"]: coupon.title,
        ["order.coupon.money"]: coupon.money
      });
    }
    var price = this.data.order.price - this.data.order.coupon.money;
    if(price <=0){
      // 用完优惠券已经抵扣完了，则显示0
      // 去掉保证金的选择
      this.setData({
        payPrice: 0,
        ["order.deposit.checked"]:false
      })
    }else{

      // 用完优惠券还不够，需要使用保证金
      if (this.data.order.deposit.checked) {
        // 已经选择上保证经了

        var value = price - this.data.order.deposit.balance
  
        if (value > 0){
          // 需支付价格 > 保证金
          this.setData({
            payPrice: value
          })
        }else{
          // 需支付价格 <= 保证金
          this.setData({
            payPrice: 0
          })
        }
      } else {
        // 没有选择保证金
        this.setData({
          payPrice: price
        })
      }

    }
    
  },
  useDeposit: function(e) {
    this.setData({
      ['order.deposit.checked']: e.detail.value
    })
    if (e.detail.value){
      // 去选中
      if(this.data.payPrice <= 0){
        // 如果优惠券已可以全部抵扣价格，则不需要再选择保证经
        this.setData({
          ['order.deposit.checked']: false
        })
      }else{
        // 优惠券不够，需要保证金抵扣
        if (this.data.order.deposit.balance >= this.data.payPrice){
          // 保证金 > 要支付的价格
          this.setData({
            payPrice: 0,
          })
        }else{
          // 保证金 < 要支付的价格
          this.setData({
            payPrice: this.data.payPrice - this.data.order.deposit.balance
          })
        }
      }
    }else{
      // 去取消选中

      var price = this.data.order.price - this.data.order.coupon.money;
      if(price <= 0 ){
        // 原价-优惠券 <= 0
        this.setData({
          payPrice: 0
        })
      }else{
        // 原价-优惠券 > 0
        this.setData({
          payPrice: price
        })
      }
    }
  },
  chooseCoupon: function(e) {
    var auction = e.currentTarget.dataset.auction;
    wx.navigateTo({
      url: '/pages/chooseCoupon/chooseCoupon?auction=' + auction
    })
  },
  getPayInfo: function() {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Pay + this.data.orderId + '/',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          order: res.data,
          payPrice: res.data.price
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
    this.setData({
      orderId: options.orderId
    });
    this.getPayInfo();
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
    this.getPayInfo();
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