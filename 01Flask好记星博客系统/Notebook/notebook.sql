/*
 Navicat MySQL Data Transfer

 Source Server         : mysql8
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost:3306
 Source Schema         : notebook

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : 65001

 Date: 15/05/2020 18:04:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for articles
-- ----------------------------
DROP TABLE IF EXISTS `articles`;
CREATE TABLE `articles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `author` varchar(255) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of articles
-- ----------------------------
BEGIN;
INSERT INTO `articles` VALUES (2, '为什么说Flask是微框架', '<h3>&ldquo;微&rdquo;并不代表整个应用只能塞在一个 Python 文件内， 当然塞在单一文件内也没有问题。 &ldquo;微&rdquo;也不代表 Flask 功能不强。 微框架中的&ldquo;微&rdquo;字表示 Flask 的目标是保持核心简单而又可扩展。 Flask 不会替你做出许多决定，比如选用何种数据库。 类似的决定，如使用何种模板引擎，是非常容易改变的。 Flask 可以变成你任何想要的东西，一切恰到好处，由你做主。</h3>\r\n\r\n<h3>缺省情况下， Flask 不包含数据库抽象层、表单验证或者其他已有的库可以处理的东西。 然而， Flask 通过扩展为你的应用添加这些功能，就如同这些功能是 Flask 生的一样。 大量的扩展用以支持数据库整合、表单验证、上传处理和各种开放验证等等。Flask 可能是 &ldquo;微小&rdquo;的，但它已经为满足您的各种生产需要做出了充足的准备。</h3>\r\n', 'andy', '2020-04-14 15:46:07');
INSERT INTO `articles` VALUES (3, 'Flask 最小应用', '<p><s>​​​​​​​​​​​​​​</s>一个最小的 Flask 应用如下:</p>\r\n\r\n<pre>\r\nfrom flask import Flask\r\napp = Flask(__name__)\r\n\r\n@app.route(&#39;/&#39;)\r\ndef hello_world():\r\n    return &#39;Hello, World!&#39;\r\n</pre>\r\n\r\n<p>那么，这些代码是什么意思呢？</p>\r\n\r\n<ol>\r\n	<li>\r\n	<p>首先我们导入了&nbsp;<a href=\"https://dormousehole.readthedocs.io/en/latest/api.html#flask.Flask\"><code>Flask</code></a>&nbsp;类。 该类的实例将会成为我们的 WSGI 应用。</p>\r\n	</li>\r\n	<li>\r\n	<p>接着我们创建一个该类的实例。第一个参数是应用模块或者包的名称。如果你使用 一个单一模块（就像本例），那么应当使用&nbsp;<code>__name__</code>&nbsp;，因为名称会根据这个 模块是按应用方式使用还是作为一个模块导入而发生变化（可能是 &lsquo;__main__&rsquo; ， 也可能是实际导入的名称）。这个参数是必需的，这样 Flask 才能知道在哪里可以 找到模板和静态文件等东西。更多内容详见&nbsp;<a href=\"https://dormousehole.readthedocs.io/en/latest/api.html#flask.Flask\"><code>Flask</code></a>&nbsp;文档。</p>\r\n	</li>\r\n	<li>\r\n	<p>然后我们使用&nbsp;<a href=\"https://dormousehole.readthedocs.io/en/latest/api.html#flask.Flask.route\"><code>route()</code></a>&nbsp;装饰器来告诉 Flask 触发函数的 URL 。</p>\r\n	</li>\r\n	<li>\r\n	<p>函数名称被用于生成相关联的 URL 。函数最后返回需要在用户浏览器中显示的信息。</p>\r\n	</li>\r\n</ol>\r\n', 'andy', '2020-04-14 15:50:38');
INSERT INTO `articles` VALUES (4, '调试模式', '<p>虽然&nbsp;<strong>flask</strong>&nbsp;命令可以方便地启动一个本地开发服务器，但是每次应用代码 修改之后都需要手动重启服务器。这样不是很方便， Flask 可以做得更好。如果你打开 调试模式，那么服务器会在修改应用代码之后自动重启，并且当应用出错时还会提供一个 有用的调试器。</p>\r\n\r\n<p>如果需要打开所有开发功能（包括调试模式），那么要在运行服务器之前导出&nbsp;<code>FLASK_ENV</code>&nbsp;环境变量并把其设置为&nbsp;<code>development</code>:</p>\r\n\r\n<pre>\r\n$ export FLASK_ENV=development\r\n$ flask run\r\n</pre>\r\n\r\n<p>（在 Windows 下需要使用&nbsp;<code>set</code>&nbsp;来代替&nbsp;<code>export</code>&nbsp;。）</p>\r\n\r\n<p>这样可以实现以下功能：</p>\r\n\r\n<ol>\r\n	<li>\r\n	<p>激活调试器。</p>\r\n	</li>\r\n	<li>\r\n	<p>激活自动重载。</p>\r\n	</li>\r\n	<li>\r\n	<p>打开 Flask 应用的调试模式。</p>\r\n	</li>\r\n</ol>\r\n\r\n<p>还可以通过导出&nbsp;<code>FLASK_DEBUG=1</code>&nbsp;来单独控制调试模式的开关。</p>\r\n', 'andy', '2020-04-15 10:32:07');
INSERT INTO `articles` VALUES (5, '路由', '<p>现代 web 应用都使用有意义的 URL ，这样有助于用户记忆，网页会更得到用户的青睐， 提高回头率。</p>\r\n\r\n<p>使用&nbsp;<a href=\"https://dormousehole.readthedocs.io/en/latest/api.html#flask.Flask.route\"><code>route()</code></a>&nbsp;装饰器来把函数绑定到 URL:</p>\r\n\r\n<pre>\r\n@app.route(&#39;/&#39;)\r\ndef index():\r\n    return &#39;Index Page&#39;\r\n\r\n@app.route(&#39;/hello&#39;)\r\ndef hello():\r\n    return &#39;Hello, World&#39;\r\n</pre>\r\n\r\n<p>但是能做的不仅仅是这些！你可以动态变化 URL 的某些部分， 还可以为一个函数指定多个规则。</p>\r\n', 'andy', '2020-04-15 10:32:27');
INSERT INTO `articles` VALUES (6, '变量规则', '<p>通过把 URL 的一部分标记为&nbsp;<code>&lt;variable_name&gt;</code>&nbsp;就可以在 URL 中添加变量。标记的 部分会作为关键字参数传递给函数。通过使用&nbsp;<code>&lt;converter:variable_name&gt;</code>&nbsp;，可以 选择性的加上一个转换器，为变量指定规则。请看下面的例子:</p>\r\n\r\n<pre>\r\n@app.route(&#39;/user/&lt;username&gt;&#39;)\r\ndef show_user_profile(username):\r\n    # show the user profile for that user\r\n    return &#39;User %s&#39; % escape(username)\r\n\r\n@app.route(&#39;/post/&lt;int:post_id&gt;&#39;)\r\ndef show_post(post_id):\r\n    # show the post with the given id, the id is an integer\r\n    return &#39;Post %d&#39; % post_id\r\n\r\n@app.route(&#39;/path/&lt;path:subpath&gt;&#39;)\r\ndef show_subpath(subpath):\r\n    # show the subpath after /path/\r\n    return &#39;Subpath %s&#39; % escape(subpath)\r\n</pre>\r\n\r\n<p>转换器类型：</p>\r\n\r\n<table>\r\n	<tbody>\r\n		<tr>\r\n			<td>\r\n			<p><code>string</code></p>\r\n			</td>\r\n			<td>\r\n			<p>（缺省值） 接受任何不包含斜杠的文本</p>\r\n			</td>\r\n		</tr>\r\n		<tr>\r\n			<td>\r\n			<p><code>int</code></p>\r\n			</td>\r\n			<td>\r\n			<p>接受正整数</p>\r\n			</td>\r\n		</tr>\r\n		<tr>\r\n			<td>\r\n			<p><code>float</code></p>\r\n			</td>\r\n			<td>\r\n			<p>接受正浮点数</p>\r\n			</td>\r\n		</tr>\r\n		<tr>\r\n			<td>\r\n			<p><code>path</code></p>\r\n			</td>\r\n			<td>\r\n			<p>类似&nbsp;<code>string</code>&nbsp;，但可以包含斜杠</p>\r\n			</td>\r\n		</tr>\r\n		<tr>\r\n			<td>\r\n			<p><code>uuid</code></p>\r\n			</td>\r\n			<td>\r\n			<p>接受 UUID 字符串</p>\r\n			</td>\r\n		</tr>\r\n	</tbody>\r\n</table>\r\n', 'andy', '2020-04-15 10:32:48');
INSERT INTO `articles` VALUES (7, '唯一的 URL / 重定向行为', '<p>以下两条规则的不同之处在于是否使用尾部的斜杠。:</p>\r\n\r\n<pre>\r\n@app.route(&#39;/projects/&#39;)\r\ndef projects():\r\n    return &#39;The project page&#39;\r\n\r\n@app.route(&#39;/about&#39;)\r\ndef about():\r\n    return &#39;The about page&#39;\r\n</pre>\r\n\r\n<p><code>projects</code>&nbsp;的 URL 是中规中矩的，尾部有一个斜杠，看起来就如同一个文件夹。 访问一个没有斜杠结尾的 URL 时 Flask 会自动进行重定向，帮你在尾部加上一个斜杠。</p>\r\n\r\n<p><code>about</code>&nbsp;的 URL 没有尾部斜杠，因此其行为表现与一个文件类似。如果访问这个 URL 时添加了尾部斜杠就会得到一个 404 错误。这样可以保持 URL 唯一，并帮助 搜索引擎避免重复索引同一页面。</p>\r\n', 'andy', '2020-04-15 10:33:03');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES (3, 'mrsoft', 'mr@mrsoft.com', '$5$rounds=535000$lDn1GaunBgX/qytv$rOSaUzYCYTon.AivhQbxaBiEgAmumU.xega9XgEFLUA');
INSERT INTO `users` VALUES (4, 'andy', 'andy@mrsoft.com', '$5$rounds=535000$lDn1GaunBgX/qytv$rOSaUzYCYTon.AivhQbxaBiEgAmumU.xega9XgEFLUA');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
