// pages/publish/publish.js
var COS = require('../../utils/cos-wx-sdk-v5.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    imageList: [],
    onlineImageList:[],
  },

  uploadImage:function(){
    var that = this;

    wx.chooseImage({
      count:9,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success:function(res){
        // 设置imageList，页面上图片自动修改。
        // that.setData({
        //   imageList: res.tempFilePaths
        // });

        // 默认图片 + 选择的图片； 
        that.setData({
          imageList: that.data.imageList.concat(res.tempFilePaths)
        });
      }
    });
  },

  uploadFile:function(){
    var onlineImageList = [];
    var that = this;
    // var cos = new COS({
    //   SecretId: 'AKIDW3Rgszw84ylQxMzNn7KOJ6kFPSL5c5MU',
    //   SecretKey: 'GQSMXmtsjR0QhuIalzTp250nU6digZSD',
    // });

    // 去某个地方获取一个临时密钥
    var cos = new COS({
      getAuthorization: function (options, callback) {
        // 服务端 JS 和 PHP 示例：https://github.com/tencentyun/cos-js-sdk-v5/blob/master/server/
        // 服务端其他语言参考 COS STS SDK ：https://github.com/tencentyun/qcloud-cos-sts-sdk
        // STS 详细文档指引看：https://cloud.tencent.com/document/product/436/14048
        wx.request({
          url: 'http://127.0.0.1:8000/api/credential/',
          data: {
            // 可从 options 取需要的参数
          },
          success: function (result) {
            var data = result.data;
            var credentials = data.credentials;
            callback({
              TmpSecretId: credentials.tmpSecretId,
              TmpSecretKey: credentials.tmpSecretKey,
              XCosSecurityToken: credentials.sessionToken,
              ExpiredTime: data.expiredTime,
            });
          }
        });
      }
    });


    for(var index in this.data.imageList){
      var filePath = this.data.imageList[index];
      cos.postObject({
        Bucket: 'mini-1251317460',
        Region: 'ap-chengdu',
        Key: index + "uuu.png",
        FilePath: filePath,
        onProgress: function (info) {
          console.log('进度条', JSON.stringify(info));
        }
      }, function (err, data) {
        onlineImageList.push(data.Location);
      });
    }
    
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