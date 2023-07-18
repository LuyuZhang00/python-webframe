// pages/newsDetail/newsDetail.js

var api = require("../../config/api.js")
var auth = require('../../utils/auth.js')
var app = getApp()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    news: {},
    isShowCommentModal: false,
    reply: null // {news,reply,nickname,content,depth}
  },

  /**
   * 点击并弹出评论对话框
   */
  onClickShowCommentModal: function(e) {
    if (!auth.authentication()) {
      return
    }
    var replyInfo = e.currentTarget.dataset;
    this.setData({
      isShowCommentModal: true,
      reply: replyInfo,
    });
  },

  /**
   * 关闭评论对话框
   */
  onClickCancelCommentModal: function() {
    this.setData({
      isShowCommentModal: false,
      reply: null
    });
  },

  /**
   * 清除回复的指定评论，变为根评论
   */
  onClickClearReply: function() {
    this.setData({
      ["reply.reply"]: null,
      ["reply.nickname"]: null,
      ["reply.depth"]: 1,
      ["reply.root"]: null,
    });
  },

  /**
   * 评论框中输入内容
   */
  inputComment: function(e) {
    this.setData({
      ["reply.content"]: e.detail.value
    });
  },
  /**
   * 点击评论发布按钮
   */
  onClickPostComment: function() {
    if (!this.data.reply) {
      wx.showToast({
        title: '请输入评论内容',
        icon: 'none'
      })
      return
    }
    if (!this.data.reply.content) {
      wx.showToast({
        title: '请输入评论内容',
        icon: 'none'
      })
      return
    }

    wx.showLoading({
      title: '发布中',
      mask: true
    })
    // 发布评论，将评论数据发送到后台接口
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Comment,
      data: this.data.reply,
      method: 'POST',
      dataType: 'json',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      responseType: 'text',
      success: (res) => {
        if (res.statusCode == 201) {
          // 发布成功
          this.setData({
            replay: null,
            isShowCommentModal: false,
            ["news.comment.count"]: this.data.news.comment.count + 1
          })
          wx.hideLoading();
          wx.showToast({
            title: '发布成功',
            icon: 'none'
          });
          // 找到位置，把最新的评论插入。
          /*
          1. 如果是根评论，直接放在最上方。
          */
          if (res.data.depth == 1) {
            var commentList = this.data.news.comment.result;
            commentList.unshift(res.data);
            this.setData({
              ["news.comment.result"]: commentList
            });
            return
          }
          /**
           * 2. 如果是非子评论，则显示在子评论的最上方
           *    - 找到根节点索引
           *    - 在child中的第一个元素插入数据
           */

          var commentList = this.data.news.comment.result;
          var commentRootIndex = this.data.reply.rootindex;
          console.log(commentList, commentRootIndex, res.data);
          var secondResultList = this.data.news.comment.result[commentRootIndex].child;
          if (secondResultList) {
            secondResultList.unshift(res.data);
          } else {
            secondResultList = [res.data]
          }
          this.setData({
            ["news.comment.result[" + commentRootIndex + "].child"]: secondResultList
          });

        }
      },
      fail: function(res) {
        wx.hideLoading()
      },
    })
  },

  /**
   * 获取更多评论
   */
  getMoreComment: function(e) {
    var rootCommentId = e.currentTarget.dataset.rootid;
    var rootCommentIndex = e.currentTarget.dataset.rootindex;
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Comment,
      data: {
        root_id: rootCommentId
      },
      method: 'GET',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        if (res.statusCode == 200) {
          this.setData({
            ["news.comment.result[" + rootCommentIndex + "].child"]: res.data
          });
        }
      },
      complete: function(res) {

      },
    })
  },

  /**
   * 评论点赞
   */
  doCommentFavor: function(e) {
    if (!auth.authentication()) {
      return
    }
    var data = e.currentTarget.dataset;
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.CommentFavor,
      data: {
        comment: data.cid
      },
      method: 'POST',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        var status;
        if (res.statusCode == 200) {
          // 取消
          status = false;
        } else if (res.statusCode == 201) {
          // 点赞
          status = true
        }
        if (data.childindex !== undefined) {
          //找到父节点下的子节点，修改状态
          console.log(data);
          this.setData({
            ["news.comment.result[" + data.rootindex + "].child[" + data.childindex + "].favor"]: status
          })

        } else {
          //找到父节点，修改状态
          this.setData({
            ["news.comment.result[" + data.rootindex + "].favor"]: status
          })
        }
      },
      complete: function(res) {},
    })
  },


  /**
   * 文章点赞
   */
  doNewsFavor: function(e) {
    if (!auth.authentication()) {
      return
    }
    var nid = e.currentTarget.dataset.nid;
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.FavorNews,
      data: {
        news: nid
      },
      method: 'POST',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        var status;
        if (res.statusCode == 200) {
          // 取消
          status = false;
        } else if (res.statusCode == 201) {
          // 点赞
          status = true
        }
        this.setData({
          ["news.favor"]: status
        })
      },
      fail: function(res) {},
      complete: function(res) {},
    })
  },

  /**
   * 关注
   */
  doFollow: function(e) {
    if (!auth.authentication()) {
      return
    }
    var userId = e.currentTarget.dataset.uid;
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.Follow,
      data: {
        user: userId
      },
      method: 'POST',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        var follow;
        if (res.statusCode == 200) {
          // 取消关注
          follow = false;
        } else if (res.statusCode == 201) {
          // 关注
          follow = true;
        }
        this.setData({
          ['news.user.follow']: follow
        });
      },
      complete: function(res) {},
    })
  },

  getNewsDetail: function(newsId) {
    var userInfo = app.globalData.userInfo;
    wx.request({
      url: api.NewsDetail + newsId + "/",
      method: 'GET',
      header: {
        Authorization: userInfo ? "token " + userInfo.token : ""
      },
      dataType: 'json',
      responseType: 'text',
      success: (res) => {
        if (res.statusCode == 200) {
          this.setData({
            news: res.data
          })
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    // 根据动态ID获取详细动态
    var newsId = options.newsId;
    this.getNewsDetail(newsId);
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

  }
})