
var app = getApp();

function is_login(){
  if(!app.globalData.userInfo){
    wx.navigateTo({
      url: '/pages/auth/auth',
    })
    return false
  }
  return true
}

module.exports = {
  is_login:is_login
}