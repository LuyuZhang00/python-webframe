// pages/auction/auction.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading:false,
    maxAuctionId:0,
    minAuctionId:0,
    auctionList:[],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

    /*
    wx.request({
      url: 'http://127.0.0.1:8000/api/auction/',
      method: 'GET',
      success: res => {
        if (res.data) {
          this.setData({ maxAuctionId: res.data[0]['id'] });
          this.setData({ minAuctionId: res.data[res.data.length-1]['id'] });
          this.setData({ auctionList: res.data });
        }
      }
    })
    */
    var new_auction_list = [
      {
        "id": 3,
        "title": "第三场 贵和祥茶道专场",
        "status": "preview",
        "status_text": "预展中",
        "look_count": 390,
        "img": "/static/images/auction/lg.png",
        "goods_count": 14,
        "total_price": 59000,
        "pics": [
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png"
        ]
      }, {
        "id": 2,
        "title": "第二场 贵和祥茶道专场",
        "status": "auction",
        "status_text": "拍卖中",
        "look_count": 390,
        "img": "/static/images/auction/lg.png",
        "goods_count": 14,
        "total_price": 59000,
        "pics": [
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png"
        ]
      },
      {
        "id": 1,
        "title": "第一场 贵和祥茶道专场",
        "status": "stop",
        "status_text": "已结束",
        "look_count": 390,
        "img": "/static/images/auction/lg.png",
        "goods_count": 14,
        "total_price": 59000,
        "pics": [
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png",
          "/static/images/auction/lg.png"
        ]
      }
    ];

    this.setData({auctionList:new_auction_list})
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
    // 下拉刷新, 获取举例当前最新之前的新数据，然后插入到页面。
    
    wx.request({
      url: 'http://127.0.0.1:8000/api/auction/',
      method: 'GET',
      data: { id_gt: this.data.maxAuctionId},
      success: res => {
        if (res.data) {
          this.setData({ maxAuctionId: res.data[0]['id'] });
          this.setData({ auctionList: res.data.concat(this.data.auctionList) });
        }
      }
    })


    wx.stopPullDownRefresh();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    // 上滑刷新
    this.setData({
      loading:true
    });
    
    wx.request({
      url: 'http://127.0.0.1:8000/api/auction/',
      method: 'GET',
      data: { id_lt:this.data.minAuctionId },
      success: res => {
        if (res.data) {
          this.setData({ minAuctionId: res.data[res.data.length - 1]['id'] });
          this.setData({ auctionList: res.data.concat(this.data.auctionList) });
        }
      }
    })


    this.setData({
      loading: false
    });
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  onClickAuctionItem:function(e){
    var autionId = e.currentTarget.dataset.aid;
    wx.navigateTo({
      url: '/pages/auctionDetail/auctionDetail?auctionId=' + autionId,
    })
  }
})