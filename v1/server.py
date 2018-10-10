"""
Creates an HTTP server with basic websocket communication.
"""
import argparse
import json
import os
import traceback
import webbrowser

import tornado.websocket

import methods
import instances_loader

from PIL import Image
import psutil

class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html", port=args.port)


class WebSocket(tornado.websocket.WebSocketHandler):

    print("WebSocket initialized")

    global data2label
    data2label = instances_loader.get_data2label()
    print("Data to label loaded")

    def on_message(self, message):
        """Evaluates the function pointed to by json-rpc."""
        print("Running on_message")
        json_rpc = json.loads(message)

        try:

            print(json_rpc["params"])
            # Get label and user info
            tweet_id = json_rpc["params"]["tweet_id"]
            label = json_rpc["params"]["label"]
            dataset = json_rpc["params"]["dataset"]
            annotator_info = json_rpc["params"]["annotator_info"]


            if label != 3 and tweet_id != 0: # 3 means user clicks "I don't Know"

                ann_path = '../../datasets/HateSPic/HateSPicLabeler/generated_json/' + dataset + '/' + tweet_id + '.json'
                # Load existing annotation (if it exists)
                if os.path.isfile(ann_path):
                    info = json.load(open(ann_path,'r'))
                    print("Updating ann file for " + str(tweet_id))

                else:
                    info = json.load(open(ann_path.replace('generated','filtered_original'),'r'))

                print("Creating new ann file for " + str(tweet_id))

                if label == 0: info['not_hate_votes'] = int(info['not_hate_votes']) + 1
                if label == 1: info['hate_votes'] = int(info['hate_votes']) + 1

                if info['voters'] != 0:
                    info['voters'] = str(info['voters']) + ',' + str(annotator_info)
                else:
                    info['voters'] = str(annotator_info)

                json.dump(info, open(ann_path,'w'))
                print("New annotation created " + str(tweet_id)) + " Label: " + str(label) + " Voters: " + str(info['voters'])

            if label == 3: # I don't know clicked
                ann_path = '../../datasets/HateSPic/HateSPicLabeler/generated_json/' + dataset + '/' + tweet_id + '.json'
                dicarded_path = '../../datasets/HateSPic/HateSPicLabeler/discarded_json/' + dataset + '/' + tweet_id + '.json'
                info = json.load(open(ann_path.replace('generated', 'filtered_original'), 'r'))
                json.dump(info, open(dicarded_path, 'w'))
                # try:
                #     os.remove(ann_path)
                #     print("Removed")
                # except:
                #     print("Could not remove")

            generated_id = getattr(methods, json_rpc["method"])(len(data2label))
            info2send = data2label[generated_id]
            error = None

        except:
            print("ERROR Writing")
            # Errors are handled by enabling the `error` flag and returning a
            # stack trace. The client can do with it what it will.
            result = traceback.format_exc()
            error = 1

        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()

        self.write_message(json.dumps({"tweet_id": str(info2send['id']), "dataset": info2send["dataset"], "img_url": info2send["img_url"], "text": info2send["text"], "error": error,
                                       "id": json_rpc["id"]},
                                      separators=(",", ":")))

        # Show local image
        image = Image.open('/home/raulgomez/datasets/HateSPic/twitter/img/' + str(info2send['id']) + '.jpg')
        image.show()

parser = argparse.ArgumentParser(description="Starts a webserver for stuff.")
parser.add_argument("--port", type=int, default=45991, help="The port on which "
                    "to serve the website.")
args = parser.parse_args()

handlers = [(r"/", IndexHandler), (r"/websocket", WebSocket),
            (r'/static/(.*)', tornado.web.StaticFileHandler,
             {'path': os.path.normpath(os.path.dirname(__file__))})]
application = tornado.web.Application(handlers)

# ADDED
# http_server = tornado.httpserver.HTTPServer(application, ssl_options={
#     "certfile": "/home/rgomez/selfsigned.crt",
#     "keyfile": "/home/rgomez/selfsigned.key",
# })

application.listen(args.port)

webbrowser.open("http://localhost:%d/" % args.port, new=2)

tornado.ioloop.IOLoop.instance().start()
