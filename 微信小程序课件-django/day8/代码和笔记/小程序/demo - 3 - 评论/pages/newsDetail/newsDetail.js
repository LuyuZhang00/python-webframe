// pages/newsDetail/newsDetail.js
var api = require("../../config/api.js")
Page({

  /**
   * 页面的初始数据
   */
  data: {
    news:null,
    isShowCommentModal:false,
    reply: {} // {depth: 1, nid: 36,content:'xx'}   {cid: 1, depth: 2, nickname: "wupeiqi", nid: 36,rid:1,content:'',rootindex:0.212}
  },
  onClickPostComment:function(){
    if(!this.data.reply.content){
      wx.showToast({
        title: '评论不能为空',
        icon: 'none'
      })
      return
    }
    
    wx.request({
      url: api.CommentAPI,
      data: {
        news:this.data.reply.nid,
        depth: this.data.reply.depth,
        reply: this.data.reply.cid, // 回复的评论id
        content: this.data.reply.content,
        root: this.data.reply.rid
      },
      method: 'POST',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        if(res.statusCode == 201){
          if (this.data.reply.rootindex == undefined){
            // 如果是根评论，应该添加到
            var dataList = this.data.news.comment;
            dataList.unshift(res.data)
            this.setData({
              ["news.comment"]: dataList,
              ["news.comment_count"]:this.data.news.comment_count + 1
            });
            this.onClickCancelCommentModal();
          }else{
            var childCommentList = this.data.news.comment[this.data.reply.rootindex].child;
            childCommentList.unshift(res.data);
            this.setData({
              ["news.comment[" + this.data.reply.rootindex + "].child"]: childCommentList,
              ["news.comment_count"]: this.data.news.comment_count + 1
            });
            this.onClickCancelCommentModal();
          }
          
          // 如果是子评论，应该添加到哪里？放在二级评论的最上方

        }
      }
    })

  },
  inputComment:function(e){
    this.setData({
      ['reply.content']: e.detail.value
    })
  },
  onClickClearReply:function(){
    this.setData({
      reply:{
        depth:1,
        nid: this.data.reply.nid
      }
    })
  },
  onClickShowCommentModal:function(e){
    this.setData({
      isShowCommentModal:true,
      reply: e.currentTarget.dataset
    })
  },
  onClickCancelCommentModal:function(){
    this.setData({
      isShowCommentModal: false,
      reply: {}
    })
  },

  getMore:function(e){
    var rootId = e.currentTarget.dataset.root;
    var idx = e.currentTarget.dataset.idx;
    /**
     *  http://127.0.0.1:8000/api/commnet/12/
     *  http://127.0.0.1:8000/api/commnet/?root=12
     */
    wx.request({
      url: api.CommentAPI,
      data: {
        root:rootId
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        // 找到跟评论下的child，把child替换为 res.data
        console.log(idx,res.data);
        this.setData({
          ["news.comment["+ idx +"].child"]:res.data
        })
      }
    })

  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var newsId = options.newsId;
    console.log(newsId);
    // 向后端发请求，获取详细信息
    wx.request({
      url: api.NewsAPI + newsId + "/",
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        this.setData({
          news:res.data
        })
      }
    })

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