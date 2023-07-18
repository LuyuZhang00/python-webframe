var settings = require('../config/settings.js')
var app = getApp()

function authentication() {
  if (!app.globalData.userInfo) {
    wx.navigateTo({
      url: settings.loginPage
    })
    return false
  }
  return true
}

module.exports = {
  authentication: authentication
}