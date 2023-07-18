//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    goodsList:[],
    seletedId:null
  },
  doPayment:function(){
    this.data.seletedId
    // 向后台发送一个请求，生成一大堆数据
    // 获取这一大堆数据，然后弹出支付二维码

    wx.request({
      url: 'http://127.0.0.1:8002/payment/',
      data: {
        goodsId: this.data.seletedId
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        console.log(res.data);
        wx.requestPayment(
          {
            'timeStamp': res.data.timeStamp,
            'nonceStr': res.data.nonceStr,
            'package': res.data.package,
            'signType': res.data.signType,
            'paySign': res.data.paySign,
            'success': function (res) {
                
             },
            'fail': function (res) {

             },
            'complete': function (res) { 

            }
          })
      }
    })

  },
  changeGoods:function(e){
    this.setData({
      seletedId: e.detail.value
    })
  },
  onLoad: function () {
    wx.request({
      url: 'http://127.0.0.1:8002/goods/',
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          goodsList:res.data
        })
      }
    })
  }
})
