const rootUrl = 'http://127.0.0.1:8000/api';

module.exports = {
  MsgCode: rootUrl + "/msg/",
  Login: rootUrl + "/login/",
  Credential: rootUrl + "/oss/credential/",
  News: rootUrl + "/news/",
  NewsDetail: rootUrl + "/news/", // 后面加ID
  Comment:rootUrl + '/comment/',
}