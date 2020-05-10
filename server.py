import tornado
from tornado.options import define, options
import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web
import os, json
from build_model import orc_img
from PIL import Image
from io import BytesIO
import base64

define("port", default=8000, help="run on the given port", type=int)




class Index(tornado.web.RequestHandler):
	def get(self):
		# self.write(json.dumps(TARGET_DATAS["list"]))
		self.render("index.html")

	def post(self):
		img = Image.open(BytesIO(base64.b64decode(self.get_argument("img").split("base64,")[1])))
		img = base64.b64encode(orc_img(img).getvalue()).decode()


		self.write(img)


def main():
	tornado.options.parse_command_line()

	http_server = tornado.httpserver.HTTPServer(
		tornado.web.Application(
			handlers=((r"/", Index),),
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "statics"),
			debug=True,

		))
	print("Development server is running at http://localhost:%s" % options.port)
	print("Quit the server with Control-C")
	http_server.listen(options.port)

	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()
