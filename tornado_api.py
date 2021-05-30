import tornado.web
import tornado.ioloop
from tensorflow.keras.models import load_model
import cv2
import string
import config
import os
import numpy as np
x="dunno"
y="dunno"
def prepare(file):
    testdata = []
    image = cv2.imread(file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    testdata.append(image);
    testdata = np.array(testdata) / 255.0
    return testdata

def predict(file):
    model = load_model('model.h5')
    prediction = model.predict([prepare(file)], verbose=0)
    global x
    print(prediction)
    if (prediction[0][0] > prediction[0][1]):
        print("Covid Possibility detected")
        x="covid"
    else:
        print("Normal xray detected")
        x="normal"
def testxray(file):
    model2 = load_model('model.h5')
    prediction = model2.predict([prepare(file)], verbose=0)
    global y
    print(prediction)
    if (prediction[0][0] > prediction[0][1]):
        print("xray")
        y = "xray"
    else:
        print("not xray")
        y = "not xray"
class uploadImgHandler(tornado.web.RequestHandler):
    def post(self):
        files = self.request.files["fileImage"]
        global x
        for f in files:

            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
            testxray(f"img/{f.filename}")
            if(y=="xray"):
                self.render("notxray.html")
            else:
                predict(f"img/{f.filename}")
        # self.write(f"http://localhost:8080/img/{f.filename}")
        if(x=="covid"):
            self.render("covid.html")
        elif(x=="normal"):
            self.render("normal.html")
        else:
            self.render("upload.html")



    def get(self):

        self.render("upload.html")


# class Application(tornado.web.Application):
#     def __init__(self):
#         handlers = [
#             (r"/", MainHandler),
#             # Add more paths here
#             (r"/KillTornado/", StopTornado),
#             (r"/tables/", ReturnQuery),
#             (r"/tables/localhost8888", MainHandler)
#         ]
#         settings = {
#             "debug": True,
#             "template_path": os.path.join(config.base_dir, "templates"),
#             "static_path": os.path.join(config.base_dir, "static")
#         }
#         tornado.web.Application.__init__(self, handlers, **settings)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/", uploadImgHandler),
            ("/img/(.*)", tornado.web.StaticFileHandler, {'path': 'img'})
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)
# if (__name__ == "__main__"):
#     app = tornado.web.Application([
#         ("/", uploadImgHandler),
#         ("/img/(.*)", tornado.web.StaticFileHandler, {'path': 'img'})
#     ])
#     settings = {
#         "static_path": os.path.join(os.path.dirname(__file__), "static")
#     }
app = tornado.httpserver.HTTPServer(Application())
app.listen(8080)
print("Listening on port 8080")
tornado.ioloop.IOLoop.instance().start()