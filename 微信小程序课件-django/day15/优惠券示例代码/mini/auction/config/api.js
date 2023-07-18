const rootUrl = 'http://127.0.0.1:8000/api';

module.exports = {
  MsgCode: rootUrl + "/msg/",
  Login: rootUrl + "/login/",
  Credential: rootUrl + "/oss/credential/",
  News: rootUrl + "/news/",
  FavorNews: rootUrl + "/news/favor/",
  NewsDetail: rootUrl + "/news/", // 后面加ID
  Comment: rootUrl + '/comment/',
  CommentFavor: rootUrl + '/comment/favor/',
  Follow: rootUrl + '/follow/',
  Auction: rootUrl + '/auction/',
  AuctionDeposit: rootUrl + '/auction/deposit/',
  PayDeposit: rootUrl + '/pay/deposit/',
  Bid: rootUrl + '/bid/',
  Coupon: rootUrl + '/coupon/',
  UserCoupon: rootUrl + '/user/coupon/',
}